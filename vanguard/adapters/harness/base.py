"""Provider-neutral harness execution boundary.

Security, authorization and durable state remain outside this adapter.
"""
from dataclasses import dataclass, field
from typing import Any, Dict, FrozenSet, Optional, Protocol, Sequence


@dataclass(frozen=True)
class PermissionContext:
    """Explicit capabilities granted to one execution request."""

    granted: FrozenSet[str] = frozenset()
    principal: str = "vanguard"

    def allows(self, capability: str) -> bool:
        return capability in self.granted


@dataclass(frozen=True)
class ExecutionRequest:
    """Normalized request independent of a concrete harness."""

    task: str
    capabilities: FrozenSet[str] = frozenset()
    permission: PermissionContext = field(default_factory=PermissionContext)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ExecutionResult:
    """Normalized outcome returned to orchestration/search layers."""

    ok: bool
    output: Any = None
    error: Optional[str] = None
    observations: Sequence[Any] = field(default_factory=tuple)
    evidence: Sequence[Any] = field(default_factory=tuple)
    cost: float = 0.0
    runtime: str = "unknown"


class HarnessRuntime(Protocol):
    def capabilities(self) -> FrozenSet[str]: ...
    def execute(self, request: ExecutionRequest) -> ExecutionResult: ...


class AuditSink(Protocol):
    def emit(self, event: Dict[str, Any]) -> None: ...


class HarnessAdapter:
    """Thin adapter that validates capability shape and normalizes execution."""

    runtime_name = "generic"

    def __init__(self, runtime: HarnessRuntime, audit: Optional[AuditSink] = None):
        self.runtime = runtime
        self.audit = audit

    def execute(self, request: ExecutionRequest) -> ExecutionResult:
        missing = [c for c in request.capabilities if not request.permission.allows(c)]
        if missing:
            result = ExecutionResult(
                ok=False,
                error=f"permission_denied:{','.join(sorted(missing))}",
                runtime=self.runtime_name,
            )
            self._audit(request, result)
            return result

        supported = self.runtime.capabilities()
        unsupported = [c for c in request.capabilities if c not in supported]
        if unsupported:
            result = ExecutionResult(
                ok=False,
                error=f"unsupported_capability:{','.join(sorted(unsupported))}",
                runtime=self.runtime_name,
            )
            self._audit(request, result)
            return result

        try:
            result = self.runtime.execute(request)
        except Exception as exc:  # defensive normalization at the adapter edge
            result = ExecutionResult(
                ok=False, error=f"runtime_error:{type(exc).__name__}:{exc}", runtime=self.runtime_name
            )
        self._audit(request, result)
        return result

    def _audit(self, request: ExecutionRequest, result: ExecutionResult) -> None:
        if self.audit is not None:
            self.audit.emit(
                {
                    "event": "harness_execution",
                    "runtime": self.runtime_name,
                    "task": request.task,
                    "capabilities": sorted(request.capabilities),
                    "principal": request.permission.principal,
                    "ok": result.ok,
                    "error": result.error,
                }
            )
