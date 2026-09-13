# VANGUARD AI v0.4 — MCTS System-Wide Architecture Contract

**Status:** PROPOSED / EXPERIMENTAL  
**Parent:** v0.3 Harness Adapter Contract  
**Change:** ADD

## Purpose

MCTS is a reusable decision/search mechanism across VANGUARD. It is not a
replacement for ORCHESTRATO, policy/security, verification, or durable
knowledge.

## System loop

```text
Goal/State -> MCTS -> abstract action/capability
           -> ORCHESTRATO Policy
           -> Adapter/Runtime
           -> Observation/Evidence
           -> Verification
           -> Reward/Value
           -> MCTS update
```

A node represents a **decision state**, not merely text. Its conceptual state
contains objective, capabilities, permissions, candidate action, observation,
verification evidence, cost/risk, visit/value statistics, and provenance.

## Search domains

The same contract can be reused for task planning, capability selection,
agent/runtime selection, tool sequences, research, and controlled evolution.
These are search domains, not automatically separate MCTS engines.

## LoRA boundary

LoRA remains a model adaptation/configuration unit. A search node may reference
a model/LoRA configuration when that configuration materially changes expected
value, cost, risk, or verification outcome:

`Node -> Model/LoRA configuration -> Action -> Observation -> Evaluation`

LoRA never gains architectural authority.

## State boundaries

MCTS state is runtime search state. It becomes knowledge only after the
existing evidence, reproduction, verification, and evaluation lifecycle.
Architectural changes require the existing reconciliation/approval process.

## Failure

Failed branches remain traceable as evidence and may contribute failure
fingerprints for recovery search. They are not silently retried as if nothing
happened.

## Non-goals

- MCTS is not declared the sole global controller.
- MCTS does not replace ORCHESTRATO or policy/security.
- DeepSeek Harness is not a core dependency.
- LoRA is not the decision engine.
