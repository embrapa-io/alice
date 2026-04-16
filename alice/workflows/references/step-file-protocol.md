# Step-File Execution Protocol

Shared reference for all Alice workflows. Step files follow this protocol unless explicitly overridden.

## Processing Rules

1. Read the entire step file before taking any action
2. Execute sections in order — never skip or reorder
3. Halt at menus and wait for user input (unless headless mode)
4. Only proceed to next step when user selects [C] Continue
5. Never load multiple step files simultaneously

## State Management

- Document every finding with file path, line number, and severity
- After completing a step, write accumulated state to disk (see `state-persistence.md`)
- At step start, check for existing state file and restore if present

## Headless Mode

When `{headless_mode}=true`:
- Auto-proceed through all [C] Continue gates
- Skip confirmations and menu displays
- Write JSON output alongside markdown

## Scope

All steps operate within the agent's `<scope-boundaries>`. Never suggest changes outside defined scope.
