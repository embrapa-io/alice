# Environment Files Validation Checklist

Shared reference for verify-compliance and code-review workflows.

## Pre-Computed Validation

If `validate-compliance.py` JSON output is available, use `checks.env` results directly.

## Required Files

- [ ] `.env.example` exists
- [ ] `.env.io.example` exists

## .env.io.example Required Variables

- [ ] `COMPOSE_PROJECT_NAME` — pattern: `{io_project}_{io_app}_{stage}`
- [ ] `COMPOSE_PROFILES` — value for the target stage
- [ ] `IO_SERVER`
- [ ] `IO_PROJECT`
- [ ] `IO_APP`
- [ ] `IO_STAGE`
- [ ] `IO_VERSION` — pattern: `0.{YY}.{M}-dev.1`
- [ ] `IO_DEPLOYER`
- [ ] `SENTRY_DSN`
- [ ] `MATOMO_ID`
- [ ] `MATOMO_TOKEN`

## Cross-File Rules

- [ ] No duplicate variable names between `.env.example` and `.env.io.example`
- [ ] No spaces around `=` in assignments
- [ ] No quotes around values (neither single nor double)
- [ ] No empty lines between related variable groups
- [ ] All IO_ variables exclusively in `.env.io.example`
- [ ] Application-specific variables exclusively in `.env.example`
