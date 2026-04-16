#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = ["pyyaml"]
# ///
"""Embrapa I/O Compliance Validator - Pre-pass deterministic validation script.

Validates a project's compliance with the Embrapa I/O platform by checking
docker-compose.yaml, environment files, .embrapa/settings.json, code patterns,
integrations, and license. Outputs a structured JSON report that an LLM agent
can consume directly, replacing 3000-5000+ tokens of manual file reading.

Usage:
    uv run validate-compliance.py --project-path /path/to/project
    uv run validate-compliance.py --project-path . --checks docker,env,settings
    uv run validate-compliance.py --project-path . --output summary
    uv run validate-compliance.py --self-test

Exit codes:
    0 = no violations found
    1 = violations found
    2 = runtime error
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

try:
    import yaml
except ImportError:
    print("Error: pyyaml is required (PEP 723 dependency)", file=sys.stderr)
    sys.exit(2)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

VALID_PLATFORMS = frozenset({
    "android", "apple", "dart", "dotnet", "electron", "elixir", "flutter",
    "go", "java", "javascript", "kotlin", "native", "node", "php", "python",
    "react-native", "ruby", "rust", "unity", "unreal",
})

VALID_VAR_TYPES = frozenset({"TEXT", "PASSWORD", "SECRET", "PORT", "VOLUME", "EMPTY"})

REQUIRED_IO_VARS = [
    "COMPOSE_PROJECT_NAME",
    "IO_SERVER",
    "IO_PROJECT",
    "IO_APP",
    "IO_STAGE",
    "IO_VERSION",
    "IO_DEPLOYER",
    "SENTRY_DSN",
    "MATOMO_ID",
]

# IO_ vars that belong exclusively in .env.io, never in .env
IO_EXCLUSIVE_VARS = frozenset({
    "COMPOSE_PROJECT_NAME", "COMPOSE_PROFILES",
    "IO_SERVER", "IO_PROJECT", "IO_APP", "IO_STAGE", "IO_VERSION", "IO_DEPLOYER",
    "SENTRY_DSN", "MATOMO_ID", "MATOMO_TOKEN",
})

REQUIRED_SETTINGS_FIELDS = [
    "boilerplate", "platform", "label", "description",
    "references", "maintainers", "variables", "orchestrators",
]

STAGE_KEYS = ["default", "alpha", "beta", "release"]

LICENSE_REQUIRED_TEXT = "Brazilian Agricultural Research Corporation (Embrapa)"

RECOMMENDED_CLI_SERVICES = frozenset({"backup", "restore", "sanitize"})

# NO-FALLBACK patterns per language
NO_FALLBACK_PATTERNS = {
    "node": [
        # process.env.X || 'default'
        (r"process\.env\.\w+\s*\|\|\s*['\"]", "process.env.VAR || 'default'"),
        # process.env.X ?? 'default'
        (r"process\.env\.\w+\s*\?\?\s*['\"]", "process.env.VAR ?? 'default'"),
    ],
    "python": [
        # os.getenv('X', 'default') or os.environ.get('X', 'default')
        (r"os\.getenv\(\s*['\"][\w]+['\"],\s*['\"]", "os.getenv('VAR', 'default')"),
        (r"os\.environ\.get\(\s*['\"][\w]+['\"],\s*['\"]", "os.environ.get('VAR', 'default')"),
    ],
    "php": [
        # getenv('X') ?: 'default'
        (r"getenv\(\s*['\"][\w]+['\"]\s*\)\s*\?:\s*['\"]", "getenv('VAR') ?: 'default'"),
        # env('X', 'default')
        (r"env\(\s*['\"][\w]+['\"],\s*['\"]", "env('VAR', 'default')"),
    ],
    "go": [
        # os.Getenv("X") with fallback assignment after
        (r'os\.Getenv\("[^"]+"\)\s*$', None),  # skip, hard to detect fallback
    ],
    "java": [
        # System.getenv("X") != null ? ... : "default"
        (r'System\.getenv\("[^"]+"\).*\?\s*.*:\s*"', 'System.getenv("VAR") with ternary fallback'),
        # Optional.ofNullable(System.getenv("X")).orElse("default")
        (r'orElse\(\s*"', 'orElse("default")'),
    ],
    "ruby": [
        # ENV['X'] || 'default'  or  ENV.fetch('X', 'default')
        (r"ENV\['\w+'\]\s*\|\|\s*['\"]", "ENV['VAR'] || 'default'"),
        (r"ENV\.fetch\(\s*['\"][\w]+['\"],\s*['\"]", "ENV.fetch('VAR', 'default')"),
    ],
}

# File extensions to scan for NO-FALLBACK by language
LANGUAGE_EXTENSIONS = {
    "node": {".js", ".ts", ".mjs", ".cjs", ".jsx", ".tsx"},
    "python": {".py"},
    "php": {".php"},
    "go": {".go"},
    "java": {".java"},
    "ruby": {".rb"},
}

# Sentry package names per ecosystem
SENTRY_PACKAGES = {
    "npm": ["@sentry/node", "@sentry/vue", "@sentry/react", "@sentry/browser",
             "@sentry/angular", "@sentry/profiling-node"],
    "composer": ["sentry/sentry", "sentry/sentry-laravel", "sentry/sentry-symfony"],
    "pip": ["sentry-sdk"],
    "go": ["github.com/getsentry/sentry-go"],
    "nuget": ["Sentry", "Sentry.AspNetCore"],
    "gem": ["sentry-ruby", "sentry-rails"],
}

# Matomo package names per ecosystem
MATOMO_PACKAGES = {
    "npm": ["vue-matomo", "matomo-tracker", "@datapunt/matomo-tracker-js",
             "matomo-tracker-react", "@jonkoops/matomo-tracker"],
    "composer": ["matomo/matomo-php-tracker"],
    "pip": [],
    "gem": [],
}


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

class Finding:
    """A single validation finding."""

    def __init__(
        self,
        rule: str,
        severity: str,
        message: str,
        file: str = "",
        line: int = 0,
        fix: str = "",
        category: str = "",
        auto_fixable: bool = False,
    ):
        self.rule = rule
        self.severity = severity
        self.message = message
        self.file = file
        self.line = line
        self.fix = fix
        self.category = category
        self.auto_fixable = auto_fixable

    def to_dict(self) -> dict:
        d: Dict[str, Any] = {
            "rule": self.rule,
            "severity": self.severity,
            "message": self.message,
        }
        if self.file:
            d["file"] = self.file
        if self.line:
            d["line"] = self.line
        if self.fix:
            d["fix"] = self.fix
        if self.auto_fixable:
            d["auto_fixable"] = True
        return d


# ---------------------------------------------------------------------------
# Utility helpers
# ---------------------------------------------------------------------------

def find_docker_compose(project: Path) -> Optional[Path]:
    """Return path to docker-compose file, preferring .yaml over .yml."""
    for name in ("docker-compose.yaml", "docker-compose.yml"):
        p = project / name
        if p.exists():
            return p
    return None


def parse_env_file(path: Path) -> List[Tuple[str, str, int]]:
    """Parse a .env file returning list of (key, value, line_number).

    Skips blank lines and comments.
    """
    entries: List[Tuple[str, str, int]] = []
    if not path.exists():
        return entries
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        for lineno, raw_line in enumerate(f, start=1):
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                continue
            key, _, value = line.partition("=")
            key = key.strip()
            value = value.strip()
            if key:
                entries.append((key, value, lineno))
    return entries


def find_line_in_file(path: Path, pattern: str) -> int:
    """Return 1-based line number of first match, or 0."""
    if not path.exists():
        return 0
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            for lineno, line in enumerate(f, start=1):
                if pattern in line:
                    return lineno
    except Exception:
        pass
    return 0


def scan_files_for_pattern(
    root: Path,
    extensions: set,
    pattern: str,
    exclude_dirs: Optional[set] = None,
    max_files: int = 500,
) -> List[Tuple[str, int, str]]:
    """Scan source files for a regex pattern. Returns [(relpath, lineno, line_text)]."""
    if exclude_dirs is None:
        exclude_dirs = {
            "node_modules", "vendor", ".git", "dist", "build",
            "__pycache__", ".next", ".nuxt", "coverage", ".embrapa",
            "_bmad", ".bmad",
        }
    results: List[Tuple[str, int, str]] = []
    compiled = re.compile(pattern)
    file_count = 0
    for ext in extensions:
        for fpath in root.rglob(f"*{ext}"):
            # Skip excluded dirs
            parts = fpath.relative_to(root).parts
            if any(p in exclude_dirs for p in parts):
                continue
            file_count += 1
            if file_count > max_files:
                return results
            try:
                with open(fpath, "r", encoding="utf-8", errors="replace") as f:
                    for lineno, line in enumerate(f, start=1):
                        if compiled.search(line):
                            rel = str(fpath.relative_to(root))
                            results.append((rel, lineno, line.rstrip()))
            except Exception:
                continue
    return results


# ---------------------------------------------------------------------------
# Stack detection
# ---------------------------------------------------------------------------

def detect_stack(project: Path) -> Dict[str, Any]:
    """Detect technology stack from project indicator files."""
    result: Dict[str, Any] = {
        "language": None,
        "framework": None,
        "detected_from": None,
        "package_manager": None,
        "database": None,
        "is_codebase": False,
    }

    # Node.js / JavaScript
    pkg_json = project / "package.json"
    if pkg_json.exists():
        try:
            with open(pkg_json, "r", encoding="utf-8") as f:
                pkg = json.load(f)
            deps = {}
            deps.update(pkg.get("dependencies", {}))
            deps.update(pkg.get("devDependencies", {}))

            result["detected_from"] = "package.json"

            # Detect framework
            if "next" in deps:
                result["framework"] = "Next.js"
                result["language"] = "javascript"
            elif "nuxt" in deps or "nuxt3" in deps:
                result["framework"] = "Nuxt"
                result["language"] = "javascript"
            elif "vue" in deps:
                result["framework"] = "Vue.js"
                result["language"] = "javascript"
                if "vuetify" in deps:
                    result["framework"] = "Vue.js + Vuetify"
            elif "react" in deps:
                result["framework"] = "React"
                result["language"] = "javascript"
            elif "angular" in deps or "@angular/core" in deps:
                result["framework"] = "Angular"
                result["language"] = "javascript"
            elif "svelte" in deps or "@sveltejs/kit" in deps:
                result["framework"] = "Svelte"
                result["language"] = "javascript"
            elif "express" in deps:
                result["framework"] = "Express"
                result["language"] = "node"
            elif "fastify" in deps:
                result["framework"] = "Fastify"
                result["language"] = "node"
            elif "@nestjs/core" in deps:
                result["framework"] = "NestJS"
                result["language"] = "node"
            else:
                result["language"] = "node"

            # Detect TypeScript
            if "typescript" in deps:
                if result["language"] == "node":
                    result["language"] = "node"  # keep as node
                # Note: TypeScript is a detail, language stays as detected

            # Detect database from deps
            if "mongoose" in deps or "mongodb" in deps:
                result["database"] = "MongoDB"
            elif "pg" in deps or "sequelize" in deps:
                result["database"] = "PostgreSQL"
            elif "mysql2" in deps or "mysql" in deps:
                result["database"] = "MySQL"
            elif "prisma" in deps or "@prisma/client" in deps:
                result["database"] = "Prisma (auto-detect)"

            # Package manager
            if (project / "pnpm-lock.yaml").exists():
                result["package_manager"] = "pnpm"
            elif (project / "yarn.lock").exists():
                result["package_manager"] = "yarn"
            elif (project / "bun.lockb").exists():
                result["package_manager"] = "bun"
            else:
                result["package_manager"] = "npm"

            result["is_codebase"] = True
            return result
        except (json.JSONDecodeError, KeyError):
            result["detected_from"] = "package.json"
            result["language"] = "node"
            result["is_codebase"] = True
            return result

    # Python
    for pyfile in ("pyproject.toml", "requirements.txt", "setup.py", "Pipfile"):
        if (project / pyfile).exists():
            result["language"] = "python"
            result["detected_from"] = pyfile
            result["is_codebase"] = True
            # Try to detect framework
            try:
                content = (project / pyfile).read_text(encoding="utf-8", errors="replace")
                if "django" in content.lower():
                    result["framework"] = "Django"
                elif "flask" in content.lower():
                    result["framework"] = "Flask"
                elif "fastapi" in content.lower():
                    result["framework"] = "FastAPI"
            except Exception:
                pass
            return result

    # PHP
    composer_json = project / "composer.json"
    if composer_json.exists():
        result["language"] = "php"
        result["detected_from"] = "composer.json"
        result["is_codebase"] = True
        try:
            with open(composer_json, "r", encoding="utf-8") as f:
                composer = json.load(f)
            reqs = {}
            reqs.update(composer.get("require", {}))
            reqs.update(composer.get("require-dev", {}))
            if "laravel/framework" in reqs:
                result["framework"] = "Laravel"
            elif "slim/slim" in reqs:
                result["framework"] = "Slim"
            elif "symfony/framework-bundle" in reqs:
                result["framework"] = "Symfony"
        except Exception:
            pass
        return result

    # Go
    if (project / "go.mod").exists():
        result["language"] = "go"
        result["detected_from"] = "go.mod"
        result["is_codebase"] = True
        return result

    # Rust
    if (project / "Cargo.toml").exists():
        result["language"] = "rust"
        result["detected_from"] = "Cargo.toml"
        result["is_codebase"] = True
        return result

    # .NET
    for csproj in project.glob("*.csproj"):
        result["language"] = "dotnet"
        result["detected_from"] = csproj.name
        result["is_codebase"] = True
        try:
            content = csproj.read_text(encoding="utf-8", errors="replace")
            if "Blazor" in content:
                result["framework"] = "Blazor"
            elif "Microsoft.AspNetCore" in content:
                result["framework"] = "ASP.NET Core"
        except Exception:
            pass
        return result

    # Java
    pom = project / "pom.xml"
    if pom.exists():
        result["language"] = "java"
        result["detected_from"] = "pom.xml"
        result["is_codebase"] = True
        return result
    gradle = project / "build.gradle"
    if gradle.exists():
        result["language"] = "java"
        result["detected_from"] = "build.gradle"
        result["is_codebase"] = True
        return result

    # Ruby
    if (project / "Gemfile").exists():
        result["language"] = "ruby"
        result["detected_from"] = "Gemfile"
        result["is_codebase"] = True
        try:
            content = (project / "Gemfile").read_text(encoding="utf-8", errors="replace")
            if "rails" in content.lower():
                result["framework"] = "Rails"
            elif "sinatra" in content.lower():
                result["framework"] = "Sinatra"
        except Exception:
            pass
        return result

    # Fallback: check docker-compose for build directives (indicates codebase)
    dc = find_docker_compose(project)
    if dc is not None:
        try:
            content = dc.read_text(encoding="utf-8", errors="replace")
            if "build:" in content or "build:" in content:
                result["is_codebase"] = True
        except Exception:
            pass

    # Also check for source files to determine codebase status
    source_exts = {".py", ".js", ".ts", ".php", ".go", ".java", ".rb", ".rs",
                   ".vue", ".jsx", ".tsx"}
    exclude = {"node_modules", "vendor", ".git", "dist", "build", "__pycache__"}
    for ext in source_exts:
        for fpath in project.rglob(f"*{ext}"):
            parts = fpath.relative_to(project).parts
            if not any(p in exclude for p in parts):
                result["is_codebase"] = True
                break
        if result["is_codebase"]:
            break

    return result


# ---------------------------------------------------------------------------
# Docker Compose validation
# ---------------------------------------------------------------------------

def validate_docker(project: Path) -> Tuple[List[Finding], Optional[str]]:
    """Validate docker-compose.yaml against Embrapa I/O rules (rules 1.1-1.15)."""
    findings: List[Finding] = []
    dc_path = find_docker_compose(project)
    dc_rel = ""

    if dc_path is None:
        findings.append(Finding(
            rule="1.1", severity="CRITICAL", category="docker",
            message="Arquivo docker-compose.yaml não encontrado na raiz do projeto",
            fix="Criar docker-compose.yaml na raiz do projeto",
        ))
        return findings, dc_rel

    dc_rel = str(dc_path.relative_to(project))
    raw_text = dc_path.read_text(encoding="utf-8", errors="replace")
    raw_lines = raw_text.splitlines()

    try:
        data = yaml.safe_load(raw_text)
    except yaml.YAMLError as e:
        findings.append(Finding(
            rule="1.1", severity="CRITICAL", category="docker",
            file=dc_rel, message=f"YAML inválido: {e}",
            fix="Corrigir sintaxe YAML do docker-compose",
        ))
        return findings, dc_rel

    if not isinstance(data, dict):
        findings.append(Finding(
            rule="1.1", severity="CRITICAL", category="docker",
            file=dc_rel, message="docker-compose.yaml não contém estrutura válida",
            fix="Corrigir estrutura do docker-compose.yaml",
        ))
        return findings, dc_rel

    # Rule 1.2: 'version' field must NOT exist
    if "version" in data:
        line = find_line_in_file(dc_path, "version:")
        findings.append(Finding(
            rule="1.2", severity="CRITICAL", category="docker",
            file=dc_rel, line=line,
            message="Campo 'version' encontrado no docker-compose.yaml (obsoleto)",
            fix="Remover campo 'version' do inicio do arquivo",
            auto_fixable=True,
        ))

    # Rules 1.3-1.5: Network 'stack'
    networks = data.get("networks", {})
    if not isinstance(networks, dict) or "stack" not in networks:
        findings.append(Finding(
            rule="1.3", severity="CRITICAL", category="docker",
            file=dc_rel,
            message="Network 'stack' não declarada em 'networks:'",
            fix="Adicionar network externa 'stack' com name: ${IO_PROJECT}_${IO_APP}_${IO_STAGE}",
            auto_fixable=True,
        ))
    else:
        stack_net = networks.get("stack", {})
        if not isinstance(stack_net, dict):
            stack_net = {}

        if not stack_net.get("external"):
            findings.append(Finding(
                rule="1.4", severity="CRITICAL", category="docker",
                file=dc_rel,
                message="Network 'stack' não está marcada como 'external: true'",
                fix="Adicionar 'external: true' na definição da network 'stack'",
                auto_fixable=True,
            ))

        net_name = stack_net.get("name", "")
        expected_name = "${IO_PROJECT}_${IO_APP}_${IO_STAGE}"
        if net_name != expected_name:
            findings.append(Finding(
                rule="1.5", severity="CRITICAL", category="docker",
                file=dc_rel,
                message=f"Network 'stack' tem name: '{net_name}' (esperado: '{expected_name}')",
                fix=f"Corrigir o 'name' da network para: {expected_name}",
            ))

    # Validate services
    services = data.get("services", {})
    if not isinstance(services, dict):
        services = {}

    # Identify CLI services (those with profiles containing 'cli')
    cli_services: set = set()
    for svc_name, svc_def in services.items():
        if not isinstance(svc_def, dict):
            continue
        profiles = svc_def.get("profiles", [])
        if isinstance(profiles, list) and "cli" in profiles:
            cli_services.add(svc_name)

    for svc_name, svc_def in services.items():
        if not isinstance(svc_def, dict):
            continue

        is_cli = svc_name in cli_services

        # Rule 1.6: All services connected to network 'stack'
        svc_networks = svc_def.get("networks", [])
        if isinstance(svc_networks, list):
            has_stack = "stack" in svc_networks
        elif isinstance(svc_networks, dict):
            has_stack = "stack" in svc_networks
        else:
            has_stack = False

        if not has_stack:
            findings.append(Finding(
                rule="1.6", severity="HIGH", category="docker",
                file=dc_rel,
                message=f"Serviço '{svc_name}' não está conectado à network 'stack'",
                fix=f"Adicionar 'stack' em 'networks:' do serviço '{svc_name}'",
            ))

        # Rule 1.7: container_name is FORBIDDEN
        if "container_name" in svc_def:
            line = find_line_in_file(dc_path, "container_name:")
            findings.append(Finding(
                rule="1.7", severity="HIGH", category="docker",
                file=dc_rel, line=line,
                message=f"Serviço '{svc_name}' usa 'container_name' (não permitido)",
                fix=f"Remover campo 'container_name' do serviço '{svc_name}'",
            ))

        # Rule 1.9: Bind mounts FORBIDDEN
        svc_volumes = svc_def.get("volumes", [])
        if isinstance(svc_volumes, list):
            for vol in svc_volumes:
                vol_str = str(vol) if not isinstance(vol, dict) else vol.get("source", "")
                # Bind mount detection: starts with ./ or / followed by :
                if isinstance(vol_str, str) and re.match(r"^(\./|/)[^:]*:", vol_str):
                    findings.append(Finding(
                        rule="1.9", severity="CRITICAL", category="docker",
                        file=dc_rel,
                        message=f"Serviço '{svc_name}' usa bind mount '{vol_str}' (não permitido)",
                        fix="Substituir bind mount por COPY no Dockerfile. Bind mounts são proibidos na plataforma Embrapa I/O.",
                    ))

        if is_cli:
            # Rule 1.13: CLI services need profiles: ['cli']
            # (already identified as CLI, but check if profiles is correct)
            restart = svc_def.get("restart")
            if restart not in ("no", '"no"', "'no'"):
                findings.append(Finding(
                    rule="1.13", severity="MEDIUM", category="docker",
                    file=dc_rel,
                    message=f"Serviço CLI '{svc_name}' sem 'restart: \"no\"' (tem: '{restart}')",
                    fix=f"Definir 'restart: \"no\"' no serviço CLI '{svc_name}'",
                ))
        else:
            # Rule 1.10: Long-running services need restart: unless-stopped
            restart = svc_def.get("restart")
            if restart != "unless-stopped":
                findings.append(Finding(
                    rule="1.10", severity="HIGH", category="docker",
                    file=dc_rel,
                    message=f"Serviço '{svc_name}' de longa duração sem 'restart: unless-stopped' (tem: '{restart}')",
                    fix=f"Adicionar 'restart: unless-stopped' ao serviço '{svc_name}'",
                ))

            # Rule 1.11: Long-running services need healthcheck
            if "healthcheck" not in svc_def:
                findings.append(Finding(
                    rule="1.11", severity="HIGH", category="docker",
                    file=dc_rel,
                    message=f"Serviço '{svc_name}' de longa duração sem 'healthcheck'",
                    fix=f"Implementar healthcheck adequado para o serviço '{svc_name}'",
                ))

    # Rule 1.12: Hardcoded ports
    for svc_name, svc_def in services.items():
        if not isinstance(svc_def, dict):
            continue
        ports = svc_def.get("ports", [])
        if isinstance(ports, list):
            for port_entry in ports:
                port_str = str(port_entry)
                # Hardcoded port: a number before the colon without ${ variable
                if re.match(r'^"?\d+:\d+"?$', port_str):
                    findings.append(Finding(
                        rule="1.12", severity="MEDIUM", category="docker",
                        file=dc_rel,
                        message=f"Serviço '{svc_name}' usa porta hardcoded: {port_str}",
                        fix="Usar variável de ambiente para mapeamento de porta: ${{SERVICE_PORT}}:{}".format(port_str.split(':')[-1].rstrip('"')),
                    ))

    # Rule 1.8: Volumes must be external
    top_volumes = data.get("volumes", {})
    if isinstance(top_volumes, dict):
        for vol_name, vol_def in top_volumes.items():
            if not isinstance(vol_def, dict):
                vol_def = {}
            if not vol_def.get("external"):
                findings.append(Finding(
                    rule="1.8", severity="HIGH", category="docker",
                    file=dc_rel,
                    message=f"Volume '{vol_name}' não está marcado como 'external: true'",
                    fix=f"Marcar volume '{vol_name}' como externo com 'external: true' e definir 'name' com padrão correto",
                    auto_fixable=True,
                ))

    # Rule 1.14: Backup volume recommended
    if isinstance(top_volumes, dict):
        has_backup_vol = any("backup" in vn.lower() for vn in top_volumes.keys())
        if not has_backup_vol and services:
            findings.append(Finding(
                rule="1.14", severity="MEDIUM", category="docker",
                file=dc_rel,
                message="Volume de backup não declarado (recomendado: backup_data)",
                fix="Adicionar volume externo 'backup_data' com name: ${IO_PROJECT}_${IO_APP}_${IO_STAGE}_backup",
            ))

    # Rule 1.15: Recommended CLI services
    present_cli = cli_services.intersection(RECOMMENDED_CLI_SERVICES)
    missing_cli = RECOMMENDED_CLI_SERVICES - present_cli
    if missing_cli:
        findings.append(Finding(
            rule="1.15", severity="LOW", category="docker",
            file=dc_rel,
            message=f"Serviços CLI recomendados não encontrados: {', '.join(sorted(missing_cli))}",
            fix="Implementar serviços CLI conforme embrapa-io-fundamentals.md",
        ))

    # Check env_file on non-CLI services
    for svc_name, svc_def in services.items():
        if not isinstance(svc_def, dict):
            continue
        if svc_name in cli_services:
            continue
        env_file = svc_def.get("env_file", [])
        if isinstance(env_file, str):
            env_file = [env_file]
        if isinstance(env_file, list):
            has_env = any(".env" == ef or ef.endswith("/.env") for ef in env_file)
            has_env_io = any(".env.io" == ef or ef.endswith("/.env.io") for ef in env_file)
            # Only flag if env_file is used at all but missing one of the pair,
            # or if neither is present (many projects use environment: instead)
            if env_file and (not has_env or not has_env_io):
                if not has_env_io:
                    findings.append(Finding(
                        rule="1.6b", severity="MEDIUM", category="docker",
                        file=dc_rel,
                        message=f"Serviço '{svc_name}' tem env_file mas falta '.env.io'",
                        fix=f"Adicionar '.env.io' em env_file do serviço '{svc_name}'",
                    ))

    return findings, dc_rel


# ---------------------------------------------------------------------------
# Environment file validation
# ---------------------------------------------------------------------------

def validate_env(project: Path) -> List[Finding]:
    """Validate .env.example and .env.io.example (rules 2.1-2.8)."""
    findings: List[Finding] = []

    env_io_example = project / ".env.io.example"
    env_example = project / ".env.example"

    # Rule 2.1: .env.io.example must exist
    if not env_io_example.exists():
        findings.append(Finding(
            rule="2.1", severity="CRITICAL", category="env",
            message="Arquivo .env.io.example não encontrado na raiz do projeto",
            fix="Criar .env.io.example com as variáveis da plataforma",
        ))
    else:
        # Rule 2.4: Required IO_ variables present
        io_entries = parse_env_file(env_io_example)
        io_keys = {e[0] for e in io_entries}

        for required_var in REQUIRED_IO_VARS:
            if required_var not in io_keys:
                findings.append(Finding(
                    rule="2.4", severity="HIGH", category="env",
                    file=".env.io.example",
                    message=f"Variável obrigatória '{required_var}' ausente em .env.io.example",
                    fix=f"Adicionar variável '{required_var}' ao .env.io.example",
                ))

        # Validate COMPOSE_PROJECT_NAME format
        for key, value, lineno in io_entries:
            if key == "COMPOSE_PROJECT_NAME":
                # Must have 3 parts separated by underscore
                parts = value.split("_")
                # Check if it has at least the pattern {project}_{app}_{stage}
                # The value itself may contain hyphens within parts
                if len(parts) < 3:
                    findings.append(Finding(
                        rule="2.6", severity="HIGH", category="env",
                        file=".env.io.example", line=lineno,
                        message=f"COMPOSE_PROJECT_NAME='{value}' não segue formato ${{IO_PROJECT}}_${{IO_APP}}_${{IO_STAGE}} (falta _${{IO_STAGE}})",
                        fix="Corrigir COMPOSE_PROJECT_NAME para o formato: {io_project}_{io_app}_{io_stage}",
                    ))

            # Validate IO_VERSION format
            if key == "IO_VERSION":
                if not re.match(r"^0\.\d{2}\.\d{1,2}-dev\.\d+$", value):
                    findings.append(Finding(
                        rule="2.4b", severity="HIGH", category="env",
                        file=".env.io.example", line=lineno,
                        message=f"IO_VERSION='{value}' não segue formato 0.YY.M-dev.N",
                        fix="Corrigir IO_VERSION para formato: 0.YY.M-dev.1 (YY=ano 2 dígitos, M=mês sem zero)",
                    ))

        # Rule 2.5: No spaces or quotes in values
        for key, value, lineno in io_entries:
            if _has_spaces_or_quotes(value):
                findings.append(Finding(
                    rule="2.5", severity="CRITICAL", category="env",
                    file=".env.io.example", line=lineno,
                    message=f"Variável '{key}' contém espaços ou aspas (não permitido)",
                    fix=f"Remover aspas e espaços do valor de '{key}'. Para valores complexos, usar Base64.",
                ))

    # Rule 2.2: .env.example must exist
    if not env_example.exists():
        findings.append(Finding(
            rule="2.2", severity="CRITICAL", category="env",
            message="Arquivo .env.example não encontrado na raiz do projeto",
            fix="Criar .env.example com as variáveis da aplicação",
        ))
    else:
        app_entries = parse_env_file(env_example)

        # Rule 2.3: No duplicate variables between .env.io and .env
        if env_io_example.exists():
            io_entries = parse_env_file(env_io_example)
            io_keys = {e[0] for e in io_entries}

            for key, value, lineno in app_entries:
                if key in IO_EXCLUSIVE_VARS or key in io_keys:
                    findings.append(Finding(
                        rule="2.3", severity="CRITICAL", category="env",
                        file=".env.example", line=lineno,
                        message=f"Variável '{key}' de .env.io está duplicada em .env.example",
                        fix=f"Remover '{key}' de .env.example (pertence ao .env.io)",
                    ))

        # Rule 2.5: No spaces or quotes in values
        for key, value, lineno in app_entries:
            if _has_spaces_or_quotes(value):
                findings.append(Finding(
                    rule="2.5", severity="CRITICAL", category="env",
                    file=".env.example", line=lineno,
                    message=f"Variável '{key}' contém espaços ou aspas (não permitido)",
                    fix=f"Remover aspas e espaços do valor de '{key}'. Para valores complexos, usar Base64.",
                ))

    # Rule 2.7: .gitignore must ignore .env, .env.io, .env.sh and AI agent dirs
    gitignore = project / ".gitignore"
    if gitignore.exists():
        try:
            gi_text = gitignore.read_text(encoding="utf-8", errors="replace")
            gi_lines = [l.strip() for l in gi_text.splitlines()]
            env_files_to_ignore = [".env", ".env.io", ".env.sh"]
            missing_env = [f for f in env_files_to_ignore if f not in gi_lines and "*.env" not in gi_lines]
            if missing_env:
                findings.append(Finding(
                    rule="2.7", severity="MEDIUM", category="env",
                    file=".gitignore",
                    message="Arquivos sensíveis não estão no .gitignore: {}".format(", ".join(missing_env)),
                    fix="Adicionar '.env', '.env.io' e '.env.sh' ao .gitignore, incluir diretórios de agentes de IA (.claude/, _bmad/, .cursor/, etc.)",
                    auto_fixable=True,
                ))
            ai_dirs_to_ignore = [
                ".agent/", ".agents/", ".augment/", ".claude/", ".cline/",
                ".codebuddy/", ".crush/", ".cursor/", ".gemini/", ".github/",
                ".iflow/", ".kilocode/", ".kiro/", ".ona/", ".opencode/",
                ".pi/", ".qoder/", ".qwen/", ".roo/", ".rovodev/",
                ".trae/", ".windsurf/", "_bmad/", "_bmad-output/",
            ]
            missing_ai = [d for d in ai_dirs_to_ignore if d not in gi_lines and d.rstrip("/") not in gi_lines]
            if missing_ai:
                findings.append(Finding(
                    rule="2.7b", severity="MEDIUM", category="env",
                    file=".gitignore",
                    message="Diretórios de agentes de IA não estão no .gitignore: {}".format(", ".join(missing_ai)),
                    fix="Adicionar diretórios de agentes de IA ao .gitignore: .claude/, _bmad/, .cursor/, .windsurf/, etc.",
                    auto_fixable=True,
                ))
        except Exception:
            pass
    else:
        findings.append(Finding(
            rule="5.2", severity="MEDIUM", category="structure",
            message="Arquivo .gitignore não encontrado",
            fix="Criar .gitignore com entradas para .env, .env.io, .env.sh e diretórios de agentes de IA",
        ))

    return findings


def _has_spaces_or_quotes(value: str) -> bool:
    """Check if an env value contains problematic spaces or quotes."""
    if not value:
        return False
    # Value wrapped in quotes
    if (value.startswith('"') and value.endswith('"')) or \
       (value.startswith("'") and value.endswith("'")):
        return True
    # Value contains unescaped spaces (not inside ${} interpolation)
    # Allow spaces in comments at end (after #)
    val_no_comment = value.split("#")[0].rstrip()
    if " " in val_no_comment:
        return True
    return False


# ---------------------------------------------------------------------------
# settings.json validation
# ---------------------------------------------------------------------------

def validate_settings(project: Path) -> List[Finding]:
    """Validate .embrapa/settings.json (rules 3.1-3.9)."""
    findings: List[Finding] = []
    settings_path = project / ".embrapa" / "settings.json"

    # Rule 3.1: File must exist
    if not settings_path.exists():
        findings.append(Finding(
            rule="3.1", severity="CRITICAL", category="settings",
            message="Arquivo .embrapa/settings.json não encontrado",
            fix="Criar .embrapa/settings.json com estrutura base",
            auto_fixable=True,
        ))
        return findings

    # Rule 3.2: Valid JSON
    try:
        with open(settings_path, "r", encoding="utf-8") as f:
            settings = json.load(f)
    except json.JSONDecodeError as e:
        findings.append(Finding(
            rule="3.2", severity="CRITICAL", category="settings",
            file=".embrapa/settings.json",
            message=f"Arquivo .embrapa/settings.json contém JSON inválido: {e}",
            fix="Corrigir sintaxe JSON do arquivo",
        ))
        return findings

    if not isinstance(settings, dict):
        findings.append(Finding(
            rule="3.2", severity="CRITICAL", category="settings",
            file=".embrapa/settings.json",
            message="settings.json não contém objeto JSON válido",
            fix="Corrigir estrutura do settings.json",
        ))
        return findings

    # Rule 3.3: Required fields
    for field in REQUIRED_SETTINGS_FIELDS:
        if field not in settings:
            findings.append(Finding(
                rule="3.3", severity="CRITICAL", category="settings",
                file=".embrapa/settings.json",
                message=f"Campo obrigatório '{field}' ausente no settings.json",
                fix=f"Adicionar campo '{field}' ao settings.json",
            ))

    # Rule 3.4: Valid platform
    platform = settings.get("platform")
    if platform is not None and platform not in VALID_PLATFORMS:
        findings.append(Finding(
            rule="3.4", severity="HIGH", category="settings",
            file=".embrapa/settings.json",
            message=f"platform '{platform}' inválida",
            fix=f"Usar um dos valores válidos: {', '.join(sorted(VALID_PLATFORMS))}",
        ))

    # Rule 3.5: variables.default must exist and not be empty
    variables = settings.get("variables")
    if isinstance(variables, dict):
        default_vars = variables.get("default")
        if default_vars is None or (isinstance(default_vars, list) and len(default_vars) == 0):
            findings.append(Finding(
                rule="3.5", severity="HIGH", category="settings",
                file=".embrapa/settings.json",
                message="variables.default ausente ou vazio no settings.json",
                fix="Adicionar array variables.default com todas as variáveis do .env",
            ))

        # Check stage keys exist
        for stage in STAGE_KEYS:
            if stage not in variables:
                findings.append(Finding(
                    rule="3.5b", severity="HIGH", category="settings",
                    file=".embrapa/settings.json",
                    message=f"variables.{stage} ausente no settings.json",
                    fix=f"Adicionar array variables.{stage} (pode ser vazio [] para stages sem overrides)",
                ))

        # Rule 3.6: Validate variable types
        for stage_key in STAGE_KEYS:
            stage_vars = variables.get(stage_key, [])
            if isinstance(stage_vars, list):
                for var_item in stage_vars:
                    if isinstance(var_item, dict):
                        var_name = var_item.get("name", "?")
                        var_type = var_item.get("type")

                        # Each variable must have name and type
                        if "name" not in var_item:
                            findings.append(Finding(
                                rule="3.6", severity="HIGH", category="settings",
                                file=".embrapa/settings.json",
                                message=f"Variável em variables.{stage_key} sem campo 'name'",
                                fix="Adicionar campo 'name' à variável",
                            ))
                        if "type" not in var_item:
                            findings.append(Finding(
                                rule="3.6", severity="HIGH", category="settings",
                                file=".embrapa/settings.json",
                                message=f"Variável '{var_name}' em variables.{stage_key} sem campo 'type'",
                                fix=f"Adicionar campo 'type' à variável '{var_name}'",
                            ))
                        elif var_type not in VALID_VAR_TYPES:
                            findings.append(Finding(
                                rule="3.6", severity="HIGH", category="settings",
                                file=".embrapa/settings.json",
                                message=f"Tipo '{var_type}' inválido para variável '{var_name}'",
                                fix=f"Usar um dos tipos válidos: {', '.join(sorted(VALID_VAR_TYPES))}",
                            ))

                        # Rule 3.7: No spaces or quotes in variable values
                        var_value = var_item.get("value", "")
                        if isinstance(var_value, str) and _has_spaces_or_quotes(var_value):
                            findings.append(Finding(
                                rule="3.7", severity="HIGH", category="settings",
                                file=".embrapa/settings.json",
                                message=f"Variável '{var_name}' contém espaços ou aspas no valor",
                                fix="Remover espaços e aspas do valor. Para valores complexos, usar Base64.",
                            ))

    # Orchestrators must contain DockerCompose
    orchestrators = settings.get("orchestrators")
    if isinstance(orchestrators, list):
        if "DockerCompose" not in orchestrators:
            findings.append(Finding(
                rule="3.8b", severity="HIGH", category="settings",
                file=".embrapa/settings.json",
                message="orchestrators não contém 'DockerCompose'",
                fix="Adicionar 'DockerCompose' ao array orchestrators",
            ))
    elif orchestrators is not None:
        findings.append(Finding(
            rule="3.8b", severity="HIGH", category="settings",
            file=".embrapa/settings.json",
            message="orchestrators deve ser um array",
            fix='Definir orchestrators como ["DockerCompose"]',
        ))

    # Rule 3.8: References empty
    references = settings.get("references")
    if isinstance(references, list) and len(references) == 0:
        findings.append(Finding(
            rule="3.8", severity="MEDIUM", category="settings",
            file=".embrapa/settings.json",
            message="Array references está vazio",
            fix="Adicionar referências técnicas relevantes ao projeto",
        ))

    # Rule 3.9: Phone format in maintainers
    maintainers = settings.get("maintainers")
    if isinstance(maintainers, list):
        phone_re = re.compile(r"^\+\d{1,3} \(\d{2}\) \d \d{4}-\d{4}$")
        for m in maintainers:
            if isinstance(m, dict):
                phone = m.get("phone", "")
                name = m.get("name", "?")
                if phone and not phone_re.match(phone):
                    findings.append(Finding(
                        rule="3.9", severity="MEDIUM", category="settings",
                        file=".embrapa/settings.json",
                        message=f"Campo 'phone' do mantenedor '{name}' não está no formato correto",
                        fix="Corrigir formato do telefone para: +DDI (DDD) X XXXX-XXXX",
                    ))

    return findings


# ---------------------------------------------------------------------------
# Code pattern validation
# ---------------------------------------------------------------------------

def validate_code(project: Path, stack: Dict[str, Any]) -> List[Finding]:
    """Validate code patterns: NO-FALLBACK, LICENSE (rules from coding standards)."""
    findings: List[Finding] = []

    # LICENSE file validation
    license_path = project / "LICENSE"
    if not license_path.exists():
        findings.append(Finding(
            rule="5.4", severity="MEDIUM", category="license",
            message="Arquivo LICENSE não encontrado",
            fix="Criar arquivo LICENSE com copyright da Embrapa",
        ))
    else:
        try:
            license_text = license_path.read_text(encoding="utf-8", errors="replace")
            if LICENSE_REQUIRED_TEXT not in license_text:
                findings.append(Finding(
                    rule="5.4b", severity="LOW", category="license",
                    file="LICENSE",
                    message="LICENSE não contém texto de copyright da Embrapa",
                    fix=f"Atualizar LICENSE para conter: 'Copyright (c) YYYY {LICENSE_REQUIRED_TEXT}. All rights reserved.'",
                ))
        except Exception:
            pass

    # NO-FALLBACK: Scan for env var access with fallback values
    language = stack.get("language")
    if language and language in NO_FALLBACK_PATTERNS:
        lang_key = language
        if language in ("javascript",):
            lang_key = "node"

        patterns = NO_FALLBACK_PATTERNS.get(lang_key, [])
        extensions = LANGUAGE_EXTENSIONS.get(lang_key, set())

        for pattern, description in patterns:
            if pattern is None or description is None:
                continue
            matches = scan_files_for_pattern(project, extensions, pattern)
            for rel_path, lineno, line_text in matches[:10]:  # cap at 10 per pattern
                findings.append(Finding(
                    rule="NO-FALLBACK", severity="HIGH", category="code",
                    file=rel_path, line=lineno,
                    message=f"Variável de ambiente com fallback/default detectada: {description}",
                    fix="Remover valor padrão. Variáveis DEVEM ser obrigatórias - se não definidas, o código DEVE falhar.",
                ))

    # README check
    if not (project / "README.md").exists():
        findings.append(Finding(
            rule="5.1", severity="MEDIUM", category="structure",
            message="Arquivo README.md não encontrado",
            fix="Criar README.md com documentação do projeto",
        ))

    return findings


# ---------------------------------------------------------------------------
# Integration detection
# ---------------------------------------------------------------------------

def validate_integrations(
    project: Path, stack: Dict[str, Any]
) -> Dict[str, Any]:
    """Detect and validate integrations: Sentry, Matomo, healthcheck."""
    result: Dict[str, Any] = {
        "sentry": {"detected": False, "package": None, "init_found": False, "findings": []},
        "matomo": {"detected": False, "package": None, "tracking_found": False, "findings": []},
        "healthcheck": {"detected": False, "endpoints": []},
    }

    is_codebase = stack.get("is_codebase", False)
    language = stack.get("language")

    # --- Sentry detection ---
    sentry_pkg_found = False
    sentry_init_found = False

    # Check package.json
    pkg_json = project / "package.json"
    if pkg_json.exists():
        try:
            with open(pkg_json, "r", encoding="utf-8") as f:
                pkg = json.load(f)
            all_deps = {}
            all_deps.update(pkg.get("dependencies", {}))
            all_deps.update(pkg.get("devDependencies", {}))
            for sentry_pkg in SENTRY_PACKAGES.get("npm", []):
                if sentry_pkg in all_deps:
                    sentry_pkg_found = True
                    result["sentry"]["package"] = sentry_pkg
                    break
        except Exception:
            pass

    # Check composer.json
    composer = project / "composer.json"
    if composer.exists() and not sentry_pkg_found:
        try:
            with open(composer, "r", encoding="utf-8") as f:
                comp = json.load(f)
            all_deps = {}
            all_deps.update(comp.get("require", {}))
            all_deps.update(comp.get("require-dev", {}))
            for sentry_pkg in SENTRY_PACKAGES.get("composer", []):
                if sentry_pkg in all_deps:
                    sentry_pkg_found = True
                    result["sentry"]["package"] = sentry_pkg
                    break
        except Exception:
            pass

    # Check requirements.txt / pyproject.toml
    for pyfile in ("requirements.txt", "pyproject.toml"):
        pf = project / pyfile
        if pf.exists() and not sentry_pkg_found:
            try:
                content = pf.read_text(encoding="utf-8", errors="replace").lower()
                if "sentry-sdk" in content or "sentry_sdk" in content:
                    sentry_pkg_found = True
                    result["sentry"]["package"] = "sentry-sdk"
            except Exception:
                pass

    # Scan source for Sentry.init / sentry initialization
    source_exts = {".js", ".ts", ".jsx", ".tsx", ".mjs", ".py", ".php", ".cs", ".go", ".rb", ".vue"}
    sentry_pattern = r"(Sentry\.init|sentry\.init|@sentry|sentry_sdk\.init|UseSentry|SentryInitializer)"
    sentry_matches = scan_files_for_pattern(project, source_exts, sentry_pattern)
    if sentry_matches:
        sentry_init_found = True

    result["sentry"]["detected"] = sentry_pkg_found or sentry_init_found
    result["sentry"]["init_found"] = sentry_init_found

    # Sentry findings
    if is_codebase and not result["sentry"]["detected"]:
        result["sentry"]["findings"].append(Finding(
            rule="4.1", severity="CRITICAL", category="integrations",
            message="Sentry não configurado (obrigatório para codebases com código-fonte)",
            fix="Implementar integração Sentry conforme stack detectada",
        ).to_dict())
    elif sentry_pkg_found and not sentry_init_found:
        result["sentry"]["findings"].append(Finding(
            rule="4.1b", severity="HIGH", category="integrations",
            message="Pacote Sentry instalado mas Sentry.init() não encontrado no código",
            fix="Configurar inicialização do Sentry no entry point da aplicação",
        ).to_dict())

    # --- Matomo detection ---
    matomo_pkg_found = False
    matomo_tracking_found = False

    # Check package.json for Matomo packages
    if pkg_json.exists():
        try:
            with open(pkg_json, "r", encoding="utf-8") as f:
                pkg = json.load(f)
            all_deps = {}
            all_deps.update(pkg.get("dependencies", {}))
            all_deps.update(pkg.get("devDependencies", {}))
            for matomo_pkg in MATOMO_PACKAGES.get("npm", []):
                if matomo_pkg in all_deps:
                    matomo_pkg_found = True
                    result["matomo"]["package"] = matomo_pkg
                    break
        except Exception:
            pass

    # Scan source for Matomo tracking
    matomo_source_exts = {".js", ".ts", ".jsx", ".tsx", ".vue", ".html", ".php"}
    matomo_pattern = r"(_paq|matomo|MATOMO_ID|hit\.embrapa\.io|MatomoTracker|MatomoInitializer|vue-matomo)"
    matomo_matches = scan_files_for_pattern(project, matomo_source_exts, matomo_pattern)
    if matomo_matches:
        matomo_tracking_found = True

    result["matomo"]["detected"] = matomo_pkg_found or matomo_tracking_found
    result["matomo"]["tracking_found"] = matomo_tracking_found

    # Matomo findings
    if is_codebase and not result["matomo"]["detected"]:
        result["matomo"]["findings"].append(Finding(
            rule="4.2", severity="CRITICAL", category="integrations",
            message="Matomo não configurado (obrigatório para codebases com código-fonte)",
            fix="Implementar tracking do Matomo conforme stack detectada",
        ).to_dict())

    # --- Healthcheck endpoint detection ---
    health_patterns = r"(/health|/healthz|/status|/api/health|/api/status|health\.php)"
    health_exts = {".js", ".ts", ".py", ".php", ".go", ".rb", ".java", ".cs"}
    health_matches = scan_files_for_pattern(project, health_exts, health_patterns)
    if health_matches:
        result["healthcheck"]["detected"] = True
        seen_endpoints: set = set()
        for rel_path, lineno, line_text in health_matches[:5]:
            ep_match = re.search(r"(/health\w*|/status|/api/health|/api/status|health\.php)", line_text)
            if ep_match:
                ep = ep_match.group(1)
                if ep not in seen_endpoints:
                    seen_endpoints.add(ep)
                    result["healthcheck"]["endpoints"].append({
                        "endpoint": ep,
                        "file": rel_path,
                        "line": lineno,
                    })

    return result


# ---------------------------------------------------------------------------
# Score calculation
# ---------------------------------------------------------------------------

def calculate_score(
    all_findings: List[Finding],
) -> Dict[str, Any]:
    """Calculate compliance score based on findings severity."""
    counts = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0}
    for f in all_findings:
        if f.severity in counts:
            counts[f.severity] += 1

    total = sum(counts.values())
    passed = 40 - total  # 40 total rules
    if passed < 0:
        passed = 0
    percentage = round((passed / 40) * 100, 1) if total <= 40 else 0.0

    # Grade: HIGH/MEDIUM/LOW per Embrapa scoring
    if counts["CRITICAL"] > 0 or counts["HIGH"] > 3:
        grade = "LOW"
    elif counts["HIGH"] > 0:
        grade = "MEDIUM"
    else:
        grade = "HIGH"

    return {
        "total_rules": 40,
        "passed": passed,
        "failed": total,
        "percentage": percentage,
        "grade": grade,
        "severity_counts": counts,
    }


# ---------------------------------------------------------------------------
# Report assembly
# ---------------------------------------------------------------------------

def build_report(
    project: Path,
    checks_filter: Optional[set],
) -> Dict[str, Any]:
    """Run all validation checks and build the JSON report."""
    report: Dict[str, Any] = {
        "project_path": str(project.resolve()),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    all_findings: List[Finding] = []

    # Stack detection (always runs)
    stack = detect_stack(project)
    report["stack"] = {
        "language": stack.get("language"),
        "framework": stack.get("framework"),
        "detected_from": stack.get("detected_from"),
        "package_manager": stack.get("package_manager"),
        "database": stack.get("database"),
        "is_codebase": stack.get("is_codebase", False),
    }

    # Initialize checks dict
    report["checks"] = {}

    # Docker validation
    if checks_filter is None or "docker" in checks_filter:
        docker_findings, dc_file = validate_docker(project)
        all_findings.extend(docker_findings)
        report["checks"]["docker"] = {
            "file": dc_file or None,
            "passed": [],
            "failed": [f.to_dict() for f in docker_findings],
        }

    # Env validation
    if checks_filter is None or "env" in checks_filter:
        env_findings = validate_env(project)
        all_findings.extend(env_findings)
        report["checks"]["env"] = {
            "passed": [],
            "failed": [f.to_dict() for f in env_findings],
        }

    # Settings validation
    if checks_filter is None or "settings" in checks_filter:
        settings_findings = validate_settings(project)
        all_findings.extend(settings_findings)
        report["checks"]["settings"] = {
            "passed": [],
            "failed": [f.to_dict() for f in settings_findings],
        }

    # Code validation
    if checks_filter is None or "code" in checks_filter:
        code_findings = validate_code(project, stack)
        all_findings.extend(code_findings)
        report["checks"]["code"] = {
            "passed": [],
            "failed": [f.to_dict() for f in code_findings],
        }

    # Integration detection
    if checks_filter is None or "integrations" in checks_filter:
        integration_result = validate_integrations(project, stack)
        # Collect integration findings into all_findings
        for key in ("sentry", "matomo"):
            for fd in integration_result[key].get("findings", []):
                all_findings.append(Finding(
                    rule=fd["rule"],
                    severity=fd["severity"],
                    message=fd["message"],
                    fix=fd.get("fix", ""),
                    category="integrations",
                ))
        report["checks"]["integrations"] = integration_result

    # Score
    if checks_filter is None or "score" in checks_filter:
        score = calculate_score(all_findings)
        report["score"] = score
        report["summary"] = score["severity_counts"]
    else:
        report["score"] = calculate_score(all_findings)
        report["summary"] = report["score"]["severity_counts"]

    return report


def format_summary(report: Dict[str, Any]) -> str:
    """Format a human-readable summary of the report."""
    lines: List[str] = []
    score = report.get("score", {})
    stack = report.get("stack", {})

    grade = score.get("grade", "?")
    grade_emoji = {"HIGH": "[CONFORME]", "MEDIUM": "[PARCIAL]", "LOW": "[NÃO CONFORME]"}.get(
        grade, "[?]"
    )

    lines.append(f"Embrapa I/O Compliance Report")
    lines.append(f"{'=' * 40}")
    lines.append(f"Projeto: {report.get('project_path', '?')}")
    lines.append(f"Data: {report.get('timestamp', '?')}")
    lines.append(f"Stack: {stack.get('language', '?')} / {stack.get('framework', '-')}")
    lines.append(f"Codebase: {'Sim' if stack.get('is_codebase') else 'Não'}")
    lines.append(f"")
    lines.append(f"Score: {grade} {grade_emoji}")
    lines.append(f"Regras: {score.get('passed', 0)}/{score.get('total_rules', 40)} aprovadas ({score.get('percentage', 0)}%)")
    lines.append(f"")

    counts = report.get("summary", {})
    lines.append(f"CRITICAL: {counts.get('CRITICAL', 0)}")
    lines.append(f"HIGH:     {counts.get('HIGH', 0)}")
    lines.append(f"MEDIUM:   {counts.get('MEDIUM', 0)}")
    lines.append(f"LOW:      {counts.get('LOW', 0)}")

    checks = report.get("checks", {})
    for cat in ("docker", "env", "settings", "code"):
        cat_data = checks.get(cat, {})
        failed = cat_data.get("failed", [])
        if failed:
            lines.append(f"")
            lines.append(f"--- {cat.upper()} ({len(failed)} findings) ---")
            for f in failed:
                sev = f.get("severity", "?")
                msg = f.get("message", "?")
                loc = ""
                if f.get("file"):
                    loc = f" [{f['file']}"
                    if f.get("line"):
                        loc += f":{f['line']}"
                    loc += "]"
                lines.append(f"  [{sev}] {msg}{loc}")

    integrations = checks.get("integrations", {})
    int_findings_count = 0
    for key in ("sentry", "matomo"):
        findings_list = integrations.get(key, {}).get("findings", [])
        int_findings_count += len(findings_list)
    if int_findings_count > 0:
        lines.append(f"")
        lines.append(f"--- INTEGRATIONS ({int_findings_count} findings) ---")
        for key in ("sentry", "matomo"):
            for f in integrations.get(key, {}).get("findings", []):
                lines.append(f"  [{f.get('severity', '?')}] {f.get('message', '?')}")

    lines.append("")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------

def run_self_test() -> bool:
    """Run built-in unit tests. Returns True if all pass."""
    import tempfile

    passed = 0
    failed = 0
    total = 0

    def assert_eq(actual: Any, expected: Any, label: str) -> None:
        nonlocal passed, failed, total
        total += 1
        if actual == expected:
            passed += 1
            print(f"  PASS: {label}", file=sys.stderr)
        else:
            failed += 1
            print(f"  FAIL: {label} (got {actual!r}, expected {expected!r})", file=sys.stderr)

    def assert_true(actual: bool, label: str) -> None:
        nonlocal passed, failed, total
        total += 1
        if actual:
            passed += 1
            print(f"  PASS: {label}", file=sys.stderr)
        else:
            failed += 1
            print(f"  FAIL: {label} (got False)", file=sys.stderr)

    def assert_contains(haystack: List[Any], needle_pred, label: str) -> None:
        nonlocal passed, failed, total
        total += 1
        if any(needle_pred(x) for x in haystack):
            passed += 1
            print(f"  PASS: {label}", file=sys.stderr)
        else:
            failed += 1
            print(f"  FAIL: {label} (not found)", file=sys.stderr)

    print("Running self-tests...\n", file=sys.stderr)

    # ---------------------------------------------------------------
    # Test 1: _has_spaces_or_quotes
    # ---------------------------------------------------------------
    print("[Test: _has_spaces_or_quotes]", file=sys.stderr)
    assert_true(_has_spaces_or_quotes('"hello"'), "quoted value detected")
    assert_true(_has_spaces_or_quotes("'hello'"), "single-quoted value detected")
    assert_true(_has_spaces_or_quotes("hello world"), "space in value detected")
    assert_true(not _has_spaces_or_quotes("hello"), "clean value accepted")
    assert_true(not _has_spaces_or_quotes(""), "empty value accepted")
    assert_true(not _has_spaces_or_quotes("hello_world"), "underscore value accepted")

    # ---------------------------------------------------------------
    # Test 2: parse_env_file
    # ---------------------------------------------------------------
    print("\n[Test: parse_env_file]", file=sys.stderr)
    with tempfile.NamedTemporaryFile(mode="w", suffix=".env", delete=False) as f:
        f.write("# comment\n")
        f.write("KEY1=value1\n")
        f.write("KEY2=value2\n")
        f.write("\n")
        f.write("KEY3=value with space\n")
        f.name
    entries = parse_env_file(Path(f.name))
    assert_eq(len(entries), 3, "parse 3 entries from env file")
    assert_eq(entries[0][0], "KEY1", "first key is KEY1")
    assert_eq(entries[0][1], "value1", "first value is value1")
    assert_eq(entries[2][2], 5, "third entry on line 5")
    os.unlink(f.name)

    # ---------------------------------------------------------------
    # Test 3: Docker validation with version field
    # ---------------------------------------------------------------
    print("\n[Test: Docker validation - version field]", file=sys.stderr)
    with tempfile.TemporaryDirectory() as tmpdir:
        dc_path = Path(tmpdir) / "docker-compose.yaml"
        dc_path.write_text(
            "version: '3.8'\nservices:\n  app:\n    image: nginx\n    networks:\n      - stack\n"
            "networks:\n  stack:\n    external: true\n    name: ${IO_PROJECT}_${IO_APP}_${IO_STAGE}\n",
            encoding="utf-8",
        )
        findings, _ = validate_docker(Path(tmpdir))
        has_version_finding = any(f.rule == "1.2" for f in findings)
        assert_true(has_version_finding, "version field detected as CRITICAL")

    # ---------------------------------------------------------------
    # Test 4: Docker validation - bind mount detection
    # ---------------------------------------------------------------
    print("\n[Test: Docker validation - bind mount detection]", file=sys.stderr)
    with tempfile.TemporaryDirectory() as tmpdir:
        dc_path = Path(tmpdir) / "docker-compose.yaml"
        dc_path.write_text(
            "services:\n  app:\n    image: nginx\n    restart: unless-stopped\n"
            "    volumes:\n      - ./data:/app/data\n    networks:\n      - stack\n"
            "    healthcheck:\n      test: curl -f http://localhost\n      interval: 10s\n"
            "networks:\n  stack:\n    external: true\n    name: ${IO_PROJECT}_${IO_APP}_${IO_STAGE}\n",
            encoding="utf-8",
        )
        findings, _ = validate_docker(Path(tmpdir))
        has_bind_mount = any(f.rule == "1.9" for f in findings)
        assert_true(has_bind_mount, "bind mount detected as CRITICAL")

    # ---------------------------------------------------------------
    # Test 5: Docker validation - container_name detection
    # ---------------------------------------------------------------
    print("\n[Test: Docker validation - container_name]", file=sys.stderr)
    with tempfile.TemporaryDirectory() as tmpdir:
        dc_path = Path(tmpdir) / "docker-compose.yaml"
        dc_path.write_text(
            "services:\n  app:\n    image: nginx\n    container_name: my-app\n"
            "    restart: unless-stopped\n    networks:\n      - stack\n"
            "    healthcheck:\n      test: curl -f http://localhost\n      interval: 10s\n"
            "networks:\n  stack:\n    external: true\n    name: ${IO_PROJECT}_${IO_APP}_${IO_STAGE}\n",
            encoding="utf-8",
        )
        findings, _ = validate_docker(Path(tmpdir))
        has_cn = any(f.rule == "1.7" for f in findings)
        assert_true(has_cn, "container_name detected as HIGH")

    # ---------------------------------------------------------------
    # Test 6: Env validation - missing files
    # ---------------------------------------------------------------
    print("\n[Test: Env validation - missing files]", file=sys.stderr)
    with tempfile.TemporaryDirectory() as tmpdir:
        findings = validate_env(Path(tmpdir))
        has_io_missing = any(f.rule == "2.1" for f in findings)
        has_env_missing = any(f.rule == "2.2" for f in findings)
        assert_true(has_io_missing, ".env.io.example missing detected")
        assert_true(has_env_missing, ".env.example missing detected")

    # ---------------------------------------------------------------
    # Test 7: Env validation - duplicate variables
    # ---------------------------------------------------------------
    print("\n[Test: Env validation - duplicate variables]", file=sys.stderr)
    with tempfile.TemporaryDirectory() as tmpdir:
        (Path(tmpdir) / ".env.io.example").write_text(
            "COMPOSE_PROJECT_NAME=proj_app_development\n"
            "IO_SERVER=localhost\nIO_PROJECT=proj\nIO_APP=app\n"
            "IO_STAGE=development\nIO_VERSION=0.26.4-dev.1\n"
            "IO_DEPLOYER=test@embrapa.br\nSENTRY_DSN=test\nMATOMO_ID=1\n",
            encoding="utf-8",
        )
        (Path(tmpdir) / ".env.example").write_text(
            "APP_PORT=3000\nIO_PROJECT=proj\n",
            encoding="utf-8",
        )
        findings = validate_env(Path(tmpdir))
        has_dup = any(f.rule == "2.3" for f in findings)
        assert_true(has_dup, "duplicate IO_PROJECT in .env.example detected")

    # ---------------------------------------------------------------
    # Test 8: Settings validation - missing file
    # ---------------------------------------------------------------
    print("\n[Test: Settings validation - missing file]", file=sys.stderr)
    with tempfile.TemporaryDirectory() as tmpdir:
        findings = validate_settings(Path(tmpdir))
        has_missing = any(f.rule == "3.1" for f in findings)
        assert_true(has_missing, "missing settings.json detected")

    # ---------------------------------------------------------------
    # Test 9: Settings validation - invalid platform
    # ---------------------------------------------------------------
    print("\n[Test: Settings validation - invalid platform]", file=sys.stderr)
    with tempfile.TemporaryDirectory() as tmpdir:
        embrapa_dir = Path(tmpdir) / ".embrapa"
        embrapa_dir.mkdir()
        (embrapa_dir / "settings.json").write_text(json.dumps({
            "boilerplate": "_",
            "platform": "invalid-platform",
            "label": "Test",
            "description": "Test project",
            "references": [],
            "maintainers": [],
            "variables": {"default": [{"name": "X", "type": "TEXT"}], "alpha": [], "beta": [], "release": []},
            "orchestrators": ["DockerCompose"],
        }), encoding="utf-8")
        findings = validate_settings(Path(tmpdir))
        has_bad_platform = any(f.rule == "3.4" for f in findings)
        assert_true(has_bad_platform, "invalid platform detected")

    # ---------------------------------------------------------------
    # Test 10: Score calculation
    # ---------------------------------------------------------------
    print("\n[Test: Score calculation]", file=sys.stderr)
    test_findings = [
        Finding(rule="t1", severity="CRITICAL", message="test"),
        Finding(rule="t2", severity="HIGH", message="test"),
    ]
    score = calculate_score(test_findings)
    assert_eq(score["grade"], "LOW", "CRITICAL + HIGH = LOW grade")

    test_findings2 = [
        Finding(rule="t1", severity="HIGH", message="test"),
    ]
    score2 = calculate_score(test_findings2)
    assert_eq(score2["grade"], "MEDIUM", "1 HIGH = MEDIUM grade")

    test_findings3: List[Finding] = []
    score3 = calculate_score(test_findings3)
    assert_eq(score3["grade"], "HIGH", "no findings = HIGH grade")

    # ---------------------------------------------------------------
    # Test 11: Stack detection
    # ---------------------------------------------------------------
    print("\n[Test: Stack detection]", file=sys.stderr)
    with tempfile.TemporaryDirectory() as tmpdir:
        (Path(tmpdir) / "package.json").write_text(json.dumps({
            "dependencies": {"express": "^4.18.0", "mongoose": "^8.0.0"},
        }), encoding="utf-8")
        stack = detect_stack(Path(tmpdir))
        assert_eq(stack["language"], "node", "Node.js detected from package.json")
        assert_eq(stack["framework"], "Express", "Express framework detected")
        assert_eq(stack["database"], "MongoDB", "MongoDB detected from mongoose")

    # ---------------------------------------------------------------
    # Test 12: Docker validation - hardcoded ports
    # ---------------------------------------------------------------
    print("\n[Test: Docker validation - hardcoded ports]", file=sys.stderr)
    with tempfile.TemporaryDirectory() as tmpdir:
        dc_path = Path(tmpdir) / "docker-compose.yaml"
        dc_path.write_text(
            "services:\n  app:\n    image: nginx\n    restart: unless-stopped\n"
            "    ports:\n      - \"3000:3000\"\n    networks:\n      - stack\n"
            "    healthcheck:\n      test: curl -f http://localhost\n      interval: 10s\n"
            "networks:\n  stack:\n    external: true\n    name: ${IO_PROJECT}_${IO_APP}_${IO_STAGE}\n",
            encoding="utf-8",
        )
        findings, _ = validate_docker(Path(tmpdir))
        has_hardcoded = any(f.rule == "1.12" for f in findings)
        assert_true(has_hardcoded, "hardcoded port detected")

    # ---------------------------------------------------------------
    # Test 13: Docker validation - non-external volume
    # ---------------------------------------------------------------
    print("\n[Test: Docker validation - non-external volume]", file=sys.stderr)
    with tempfile.TemporaryDirectory() as tmpdir:
        dc_path = Path(tmpdir) / "docker-compose.yaml"
        dc_path.write_text(
            "services:\n  app:\n    image: nginx\n    restart: unless-stopped\n"
            "    volumes:\n      - data:/app/data\n    networks:\n      - stack\n"
            "    healthcheck:\n      test: curl -f http://localhost\n      interval: 10s\n"
            "networks:\n  stack:\n    external: true\n    name: ${IO_PROJECT}_${IO_APP}_${IO_STAGE}\n"
            "volumes:\n  data:\n    driver: local\n",
            encoding="utf-8",
        )
        findings, _ = validate_docker(Path(tmpdir))
        has_non_ext = any(f.rule == "1.8" for f in findings)
        assert_true(has_non_ext, "non-external volume detected")

    # ---------------------------------------------------------------
    # Test 14: Env validation - spaces/quotes in values
    # ---------------------------------------------------------------
    print("\n[Test: Env validation - spaces/quotes in values]", file=sys.stderr)
    with tempfile.TemporaryDirectory() as tmpdir:
        (Path(tmpdir) / ".env.io.example").write_text(
            "COMPOSE_PROJECT_NAME=proj_app_development\n"
            "IO_SERVER=localhost\nIO_PROJECT=proj\nIO_APP=app\n"
            "IO_STAGE=development\nIO_VERSION=0.26.4-dev.1\n"
            "IO_DEPLOYER=test@embrapa.br\nSENTRY_DSN=test\nMATOMO_ID=1\n",
            encoding="utf-8",
        )
        (Path(tmpdir) / ".env.example").write_text(
            'DB_NAME="my database"\nAPP_PORT=3000\n',
            encoding="utf-8",
        )
        findings = validate_env(Path(tmpdir))
        has_quotes = any(f.rule == "2.5" and "DB_NAME" in f.message for f in findings)
        assert_true(has_quotes, "quoted value with spaces detected")

    # ---------------------------------------------------------------
    # Test 15: Settings validation - invalid variable type
    # ---------------------------------------------------------------
    print("\n[Test: Settings validation - invalid variable type]", file=sys.stderr)
    with tempfile.TemporaryDirectory() as tmpdir:
        embrapa_dir = Path(tmpdir) / ".embrapa"
        embrapa_dir.mkdir()
        (embrapa_dir / "settings.json").write_text(json.dumps({
            "boilerplate": "_",
            "platform": "node",
            "label": "Test",
            "description": "Test project",
            "references": [],
            "maintainers": [],
            "variables": {
                "default": [{"name": "X", "type": "INVALID_TYPE"}],
                "alpha": [], "beta": [], "release": [],
            },
            "orchestrators": ["DockerCompose"],
        }), encoding="utf-8")
        findings = validate_settings(Path(tmpdir))
        has_bad_type = any(f.rule == "3.6" and "INVALID_TYPE" in f.message for f in findings)
        assert_true(has_bad_type, "invalid variable type detected")

    # ---------------------------------------------------------------
    # Test 16: Settings validation - phone format
    # ---------------------------------------------------------------
    print("\n[Test: Settings validation - phone format]", file=sys.stderr)
    with tempfile.TemporaryDirectory() as tmpdir:
        embrapa_dir = Path(tmpdir) / ".embrapa"
        embrapa_dir.mkdir()
        (embrapa_dir / "settings.json").write_text(json.dumps({
            "boilerplate": "_",
            "platform": "node",
            "label": "Test",
            "description": "Test project",
            "references": [],
            "maintainers": [
                {"name": "Test User", "email": "test@embrapa.br", "phone": "5567981118060"},
            ],
            "variables": {"default": [{"name": "X", "type": "TEXT"}], "alpha": [], "beta": [], "release": []},
            "orchestrators": ["DockerCompose"],
        }), encoding="utf-8")
        findings = validate_settings(Path(tmpdir))
        has_phone = any(f.rule == "3.9" for f in findings)
        assert_true(has_phone, "invalid phone format detected")

    # ---------------------------------------------------------------
    # Summary
    # ---------------------------------------------------------------
    print(f"\n{'=' * 40}", file=sys.stderr)
    print(f"Self-test results: {passed}/{total} passed, {failed} failed", file=sys.stderr)

    return failed == 0


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Embrapa I/O Compliance Validator.\n"
            "Validates a project against 40 Embrapa I/O platform rules and outputs "
            "a structured JSON report for LLM agent consumption."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  uv run validate-compliance.py --project-path /path/to/project\n"
            "  uv run validate-compliance.py --project-path . --checks docker,env\n"
            "  uv run validate-compliance.py --project-path . --output summary\n"
            "  uv run validate-compliance.py --self-test\n"
        ),
    )
    parser.add_argument(
        "--project-path",
        help="Path to the project root (required unless --self-test)",
    )
    parser.add_argument(
        "--checks",
        help="Comma-separated list of check categories to run. "
        "Options: docker, env, settings, code, integrations, score. "
        "Default: all checks.",
    )
    parser.add_argument(
        "--output",
        choices=["json", "summary"],
        default="json",
        help="Output format: json (machine-readable) or summary (human-readable). Default: json.",
    )
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="Run built-in unit tests and exit.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.self_test:
        success = run_self_test()
        sys.exit(0 if success else 1)

    if not args.project_path:
        print("Error: --project-path is required (use --self-test for testing)", file=sys.stderr)
        sys.exit(2)

    project = Path(args.project_path).resolve()
    if not project.is_dir():
        print(f"Error: '{project}' is not a directory", file=sys.stderr)
        sys.exit(2)

    checks_filter: Optional[set] = None
    if args.checks:
        checks_filter = {c.strip().lower() for c in args.checks.split(",")}
        valid_checks = {"docker", "env", "settings", "code", "integrations", "score"}
        invalid = checks_filter - valid_checks
        if invalid:
            print(f"Error: invalid check categories: {', '.join(invalid)}", file=sys.stderr)
            print(f"Valid options: {', '.join(sorted(valid_checks))}", file=sys.stderr)
            sys.exit(2)

    try:
        report = build_report(project, checks_filter)
    except Exception as e:
        print(f"Error: runtime exception: {e}", file=sys.stderr)
        sys.exit(2)

    if args.output == "json":
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(format_summary(report))

    # Exit code based on findings
    total_failed = report.get("score", {}).get("failed", 0)
    sys.exit(1 if total_failed > 0 else 0)


if __name__ == "__main__":
    main()
