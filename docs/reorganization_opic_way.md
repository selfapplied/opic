# Reorganization: The OPIC Way

## Principle

**Use OPIC to organize OPIC.** Instead of Python scripts, we define reorganization as voices.

## Structure

### Core Files

- `systems/reorganize.ops` — Core reorganization voices
- `systems/reorganize_plan.ops` — Planning and classification
- `systems/reorganize_execute.ops` — Step-by-step execution

## How It Works

### 1. Structure Definition

Voices define the new structure:

```ops
voice create.core.structure / {
  core_dir -> 
  create.directory -> 
  move.opic_executor -> 
  move.parser -> 
  core_ready
}
```

### 2. File Classification

Voices classify files by domain:

```ops
voice domain.01_ce1 / {
  file -> 
  check.includes.ce1 -> 
  check.includes.pascal -> 
  check.includes.zeta -> 
  is_ce1
}
```

### 3. Migration Execution

Voices execute migration step-by-step:

```ops
voice execute.reorganization / {
  current_state -> 
  step.1.create.structure -> 
  step.2.classify.files -> 
  step.3.migrate.core -> 
  step.4.migrate.systems -> 
  step.5.migrate.docs -> 
  step.6.archive.experiments -> 
  step.7.update.references -> 
  step.8.validate -> 
  reorganization_executed
}
```

## Execution

```bash
# Review the plan
opic execute systems/reorganize_plan.ops

# Execute reorganization
opic execute systems/reorganize_execute.ops
```

## Benefits

1. **Language-first**: OPIC manages itself
2. **Composable**: Voices can be combined
3. **Reversible**: Each step can be undone
4. **Self-documenting**: The plan is executable code
5. **Testable**: Validate structure through voices

## Next Steps

1. Implement the actual file operations in the executor
2. Add validation voices
3. Create dry-run mode
4. Execute when ready

