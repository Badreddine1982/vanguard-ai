"""Minimal deterministic selection scaffold for the VANGUARD MCTS boundary.

This is deliberately not the final optimizer. It establishes the contract so
ORCHESTRATO, verification, and adapters can evolve independently.
"""
from typing import Iterable, List, Optional

from .contracts import ActionCandidate, SearchResult, SearchState, TreeNode, ValueEvaluator


class MCTSController:
    def __init__(self, evaluator: Optional[ValueEvaluator] = None):
        self.evaluator = evaluator or (lambda _state, _action: 0.0)

    def select(self, state: SearchState, actions: Iterable[ActionCandidate]) -> SearchResult:
        candidates: List[ActionCandidate] = list(actions)
        if not candidates:
            return SearchResult(action=None, value=0.0, visits=0, trace=(state.state_id,))

        root = TreeNode(state=state)
        scored = []
        for action in candidates:
            value = float(self.evaluator(state, action))
            child = TreeNode(state=state, action=action, parent=root, visits=1, value=value)
            root.children.append(child)
            scored.append((value, action, child))

        best_value, best_action, best_node = max(
            scored, key=lambda item: (item[0], item[1].action_id)
        )
        return SearchResult(
            action=best_action,
            value=best_value,
            visits=best_node.visits,
            trace=(state.state_id, best_action.action_id),
        )
