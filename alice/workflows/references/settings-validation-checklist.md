# Settings.json Validation Checklist

Shared reference for verify-compliance and code-review workflows.

## Pre-Computed Validation

If `validate-compliance.py` JSON output is available, use `checks.settings` results directly.

## File Location

- [ ] `.embrapa/settings.json` exists
- [ ] File is valid JSON (parseable without errors)

## Required Fields

- [ ] `boilerplate` — string, typically `"_"`
- [ ] `platform` — string, detected platform identifier
- [ ] `label` — string, project display name
- [ ] `description` — string, project description
- [ ] `references` — array of `{ "label": string, "url": string }`
- [ ] `maintainers` — array of `{ "name": string, "email": string, "phone": string }`
- [ ] `variables` — object with stage keys
- [ ] `orchestrators` — array, must contain `"DockerCompose"`

## Variables Structure

- [ ] `variables.default` exists and is an array
- [ ] `variables.alpha` exists and is an array
- [ ] `variables.beta` exists and is an array
- [ ] `variables.release` exists and is an array
- [ ] Each variable entry has `name` (string) and `type` (string) fields
