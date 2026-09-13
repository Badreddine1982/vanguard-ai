# VANGUARD AI — Foundation Repository v0.1

This branch establishes the implementation track for the current VANGUARD
architecture without deleting or silently rewriting the existing VANGUARD Pro
implementation on `main`.

## Source-of-truth separation

- **Architecture / governance library:** design authority.
- **GitHub repository:** executable implementation and integration evidence.
- **`tests/`:** verification evidence.
- **`experiments/`:** research prototypes that are not yet production modules.

## Foundation layout

```text
vanguard/
  core/            runtime state contracts
  mcts/            system-wide decision/search contracts
  adapters/        provider-neutral execution boundaries
    harness/       DeepSeek/compatible harness bindings

tests/foundation/  foundation verification

docs/
  architecture/   approved/proposed architecture contracts
  governance/     update and evolution rules

experiments/       experimental MCTS/T5/RL work
```

## Integration rule

The existing root-level implementation remains untouched in this foundation
branch. New architecture enters through the `vanguard/` namespace and is
promoted only after tests, verification, and architecture compatibility checks.

This avoids a destructive migration and prevents two implementations from
being silently treated as one runtime.
