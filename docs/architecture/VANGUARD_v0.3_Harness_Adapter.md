# VANGUARD AI v0.3 — Harness Adapter Contract

**Status:** EXPERIMENTAL IMPLEMENTATION  
**Change:** ADD

## Boundary

External agent runtimes are adapters. DeepSeek Harness is one implementation,
not a VANGUARD core dependency.

```text
ORCHESTRATO
  -> Policy / Session / Audit
  -> Harness Adapter
  -> DeepSeek Harness / Claude Code / other runtime
  -> normalized observation/result
```

## Contract

The adapter boundary exposes normalized execution requests/results and keeps
runtime-specific details out of VANGUARD state semantics.

Permissions are explicit and propagated into the request. Policy authority is
not duplicated inside the adapter. Audit receives normalized execution events.

## Subagents and hooks

Harness subagents and lifecycle hooks may be used as integration mechanisms,
but they do not become the VANGUARD security authority. Child execution must
receive only explicitly granted capabilities.

## Trust boundary

Harness output is evidence/observation, not automatically trusted knowledge.
Internalization requires reconstruction/reproduction, verification, evaluation,
and only then promotion to durable knowledge.

## Verification

The foundation adapter is covered by tests for permission propagation,
permission denial, unsupported capabilities, successful normalization/audit,
and runtime-failure normalization.
