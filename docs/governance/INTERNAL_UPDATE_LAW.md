# LIBRARY_INTERNAL_UPDATE_LAW

This repository copy records the implementation-side rule. It does not
replace the architectural Master Page or the project library.

## Rules

1. Architecture and governance changes are documented before implementation.
2. Existing working code is not silently overwritten by a new architecture.
3. Experimental code stays under `experiments/` until it passes integration gates.
4. Production modules live under `vanguard/` and must have verification evidence.
5. Tests are evidence, not architectural authority.
6. External runtimes remain adapters; policy, audit, and state authority stay in
   the VANGUARD/ORCHESTRATO control plane.
7. MCTS may search decisions but cannot authorize actions or promote knowledge.
8. LoRA is an adaptation/configuration unit, not the global controller.
9. Failed experiments remain traceable and are not silently treated as success.

## Foundation update

**ID:** REPO-0001  
**Scope:** Establish GitHub implementation track  
**Branch:** `vanguard-foundation-v0.1`

Implemented: provider-neutral Harness Adapter boundary, DeepSeek Harness
binding, system-wide MCTS contracts, minimal MCTS selection scaffold, and
foundation tests.

The existing root-level VANGUARD Pro implementation on `main` remains
untouched. Migration is intentionally deferred until compatibility and
verification gates are satisfied.
