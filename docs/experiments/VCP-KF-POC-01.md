# VCP/KF-POC-01 — Cross-Repository Knowledge + Compatibility Fabric

Status: **EXPERIMENT / HYPOTHESIS**

## Objective

Test whether independent repositories can exchange reusable knowledge
(seeds, patterns, evidence) while retaining independent protected state,
execution authority, and acceptance decisions.

## Core hypothesis

Knowledge can cross repository boundaries; authority must not.

## Governing library law — Evidence-Gated Persistence

> **Probability may enter the loop, but it does not leave the loop as truth without confirmation.**

Every hypothesis, probability, or candidate pattern that enters the knowledge
loop must leave a durable trace. Its long-term state is one of:

- **confirmed fact** — independently reproduced and/or formally verified, with provenance;
- **potential error** — not confirmed, contradicted, or architecturally suspect, but retained as a reusable warning/evidence record.

A failed experiment is therefore **not discarded by default**. The failure,
its observed conditions, provenance, and current interpretation are retained
so later experiments can reuse the evidence.

**No confirmation, no adoption.**

The following are deliberately *not* decided by this law:

- pruning policy;
- deletion/retention rights beyond durable evidence preservation;
- whether the current architecture is the correct layer for pruning;
- final authority for changing or removing historical evidence.

Those are deferred architectural questions and must be reviewed separately.

## Loop model

```
Internal Loop
MCTS → Seed/Pattern → VERITAS/Lean → Evidence
                                      │
                                      ▼
                              Knowledge Fabric
                                      │
                     ┌────────────────┴────────────────┐
                     ▼                                 ▼
              confirmed fact                    potential error
                     │                                 │
                     └────────── durable knowledge ────┘
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
- confirmed facts
- potential-error records

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
- evidence-gated persistence rule
- potential-error retention record

## Acceptance rule

A knowledge artifact remains `hypothesis` until independent reproduction
and verification produce sufficient evidence. A successful CI run proves
schema/structure validity only; it does not prove the architectural
hypothesis.

A failure may be promoted to a **potential-error record** when it is
reproducible or otherwise supported by traceable evidence. This preserves
the information value of failure without treating the suspected cause as
fact.

## Next experiment

When `vanguard-contracts` and `vanguard-runtime` exist, extend this POC
with:

1. contract-change event
2. affected-component discovery
3. compatibility test dispatch
4. cross-repository evidence artifact
5. independent reproduction
6. generated compatibility matrix
7. propagation of confirmed facts and potential-error records

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

The governing law itself should likewise be treated as a proposed library
law until the broader library review confirms it.
