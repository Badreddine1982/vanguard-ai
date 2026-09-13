"""Small, provider-neutral MCTS data contracts."""
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Tuple


@dataclass(frozen=True)
class SearchState:
    """Runtime search state; it is not durable knowledge or architecture state."""

    state_id: str
    objective: str
    payload: Any = None


@dataclass(frozen=True)
class ActionCandidate:
    action_id: str
    description: str
    payload: Any = None


@dataclass
class TreeNode:
    state: SearchState
    action: Optional[ActionCandidate] = None
    parent: Optional["TreeNode"] = None
    children: List["TreeNode"] = field(default_factory=list)
    visits: int = 0
    value: float = 0.0
    observations: List[Any] = field(default_factory=list)
    verification: Optional[Any] = None

    @property
    def mean_value(self) -> float:
        return self.value / self.visits if self.visits else 0.0


@dataclass(frozen=True)
class SearchResult:
    action: Optional[ActionCandidate]
    value: float
    visits: int
    trace: Tuple[str, ...] = ()


ValueEvaluator = Callable[[SearchState, ActionCandidate], float]
