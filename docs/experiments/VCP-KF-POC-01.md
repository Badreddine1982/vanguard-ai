# VCP/KF-POC-01 — Cross-Repository Knowledge + Compatibility Fabric

Status: **EXPERIMENT / HYPOTHESIS**

## Objective

Test whether independent repositories can exchange reusable knowledge
(seeds, patterns, evidence) while retaining independent protected state,
execution authority, and acceptance decisions.

## Core hypothesis

Knowledge can cross repository boundaries; authority must not.

## Loop model

```
Internal Loop
MCTS → Seed/Pattern → VERITAS/Lean → Evidence
                                      │
                                      ▼
                              Knowledge Fabric
                                      │
                                      ▼
External Loop
Repository → Contract/Integration Test → Evidence
                                      │
                                      └──────→ Internal Loop
```

## Shared

- seeds
- patterns
- evidence
- proof artifacts
- benchmarks
- provenance
- compatibility observations

## Not shared

- secrets
- protected runtime state
- credentials
- execution authority
- final merge authority

## Current POC boundary

The connected GitHub workspace currently exposes `vanguard-ai` for this
experiment. The planned `vanguard-contracts` and `vanguard-runtime`
components are therefore represented as protocol targets, not fabricated
repositories. This distinction is intentional: absence of evidence is not
treated as evidence of implementation.

## Implemented

- `.vanguard/component.yaml`
- versioned knowledge artifact
- dependency-free structural validator
- GitHub Actions validation workflow
- explicit hypothesis/promotion boundary

## Acceptance rule

A knowledge artifact remains `hypothesis` until independent reproduction
and verification produce sufficient evidence. A successful CI run proves
schema/structure validity only; it does not prove the architectural
hypothesis.

## Next experiment

When `vanguard-contracts` and `vanguard-runtime` exist, extend this POC
with:

1. contract-change event
2. affected-component discovery
3. compatibility test dispatch
4. cross-repository evidence artifact
5. independent reproduction
6. generated compatibility matrix

## Result interpretation

PASS of the validator means:

- the repository declares the protocol boundary correctly;
- the knowledge artifact is structurally valid;
- the promotion gate is present.

It does **not** mean:

- the knowledge is true;
- repositories are compatible;
- VERITAS has accepted the pattern;
- execution authority has crossed a repository boundary.

## Long-term promotion candidate

If repeated independent experiments support the hypothesis, the protocol
may be promoted into VERITAS-AIXI architecture documentation. Until then,
this file remains an experimental record.
