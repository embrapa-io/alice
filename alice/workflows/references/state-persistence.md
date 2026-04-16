# State Persistence Protocol

Shared reference for all core workflows (VC, IA, CR). Prevents data loss from context compaction during multi-step workflows.

## Why

Alice workflows accumulate findings across 5-6 steps in conversational context. If context compaction occurs mid-workflow, findings from earlier steps can be silently lost, corrupting the final report. Writing intermediate state to disk ensures resilience.

## Protocol

### State File

Each workflow writes intermediate state to a temporary file at `{project-root}/_bmad-output/.alice-state-{workflow-name}.json`.

### When to Write

After each step completes (before loading the next step file), write the current accumulated state:

```json
{
  "workflow": "verify-compliance",
  "timestamp": "ISO-8601",
  "current_step": "step-02-validate-docker",
  "completed_steps": ["step-01-analyze-codebase"],
  "findings": [
    { "step": "step-01", "category": "stack", "data": "..." },
    { "step": "step-02", "category": "docker", "data": "..." }
  ],
  "variables": {
    "detected_stack": "node",
    "has_docker_compose": true
  }
}
```

### When to Read

At the start of each step, if the state file exists, read and restore accumulated findings. This enables recovery if the session was interrupted.

### Cleanup

The final step of each workflow deletes the state file after the report is successfully written.

## Headless Mode Integration

In headless mode, the state file doubles as progress tracking. The JSON structure matches the headless output schema, enabling CI tools to monitor progress.
