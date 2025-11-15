# How opic Execution Works

## Overview

opic executes voice chains using a sequential, recursive model with automatic voice discovery.

## Execution Flow

### 1. Parse Chain

```
Input: {step1 -> step2 -> step3}
↓
Parse: Remove braces, split by "->"
↓
Steps: ["step1", "step2", "step3"]
```

### 2. Discover Voices

Based on chain context, automatically discover relevant voices:
- Keywords in steps → discover matching voice namespaces
- Example: "cycle promote" → discovers `cycle.*` voices

### 3. Execute Steps Sequentially

For each step:

```
Step: "reason.understand"
↓
Check: Is it in voices?
  ✓ Yes → Get voice body
  ✗ No → Try discovered voices
  ✗ No → Use as literal value
↓
If voice body is chain: {nested -> chain}
  → Recursively execute nested chain
↓
If voice body is value: "some value"
  → Use as result
↓
Pass result to next step
```

### 4. Data Flow

- Each step receives the **result** of the previous step
- Nested chains receive inputs via `{"input": previous_result}`
- Final result is the last step's output

## Example

```ops
voice main / {reason.toward_goal -> reason.plan -> reason.verify}
```

**Execution:**

1. **Parse**: `["reason.toward_goal", "reason.plan", "reason.verify"]`

2. **Step 1: `reason.toward_goal`**
   - Found in voices: `{goal + current_state -> gap -> action}`
   - Is chain → recurse
   - Execute: `goal + current_state -> gap -> action`
   - Result: `"action"`

3. **Step 2: `reason.plan`**
   - Found in voices: `{goal + constraints -> decompose -> steps}`
   - Is chain → recurse
   - Execute: `goal + constraints -> decompose -> steps`
   - Result: `"steps"`

4. **Step 3: `reason.verify`**
   - Found in voices: `{claim + evidence -> verified}`
   - Is chain → recurse
   - Execute: `claim + evidence -> verified`
   - Result: `"verified"`

5. **Final result**: `"verified"`

## Automatic Voice Discovery

During execution, opic discovers relevant voices:

- **Context**: `"reason.toward_goal reason.plan reason.verify"`
- **Keywords**: None match discovery patterns
- **Discovered**: `[]` (no matches)

If context was `"learn energy density"`:
- **Discovered**: All `thermo.*` voices (47 voices)
- **Available**: Can be used if step not found

## Current Behavior

**What works:**
- ✅ Parses chains correctly
- ✅ Executes steps sequentially
- ✅ Handles nested chains recursively
- ✅ Discovers voices automatically
- ✅ Returns final result

**What's limited:**
- ⚠️ Execution is silent (no output)
- ⚠️ Discovered voices aren't automatically composed
- ⚠️ Steps that aren't voices become literal strings
- ⚠️ No actual computation happens (just string flow)

## The Gap

The execution **structure** works, but:
- Voices are declarative (just chains/strings)
- No actual computation logic
- Results are just step names, not computed values

This is why benchmarks score low - the execution framework exists, but the voices don't actually compute anything yet.

