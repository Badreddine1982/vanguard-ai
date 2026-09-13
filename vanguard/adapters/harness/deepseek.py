"""DeepSeek Harness binding kept behind the generic adapter contract."""
from typing import Optional

from .base import AuditSink, ExecutionRequest, ExecutionResult, HarnessAdapter, HarnessRuntime


class DeepSeekHarnessAdapter(HarnessAdapter):
    """Adapter for a DeepSeek Harness-compatible runtime.

    The runtime object is injected so the core does not depend on a specific
    SDK, process launcher, or network transport.
    """

    runtime_name = "deepseek-harness"

    def __init__(self, runtime: HarnessRuntime, audit: Optional[AuditSink] = None):
        super().__init__(runtime=runtime, audit=audit)

    def execute(self, request: ExecutionRequest) -> ExecutionResult:
        return super().execute(request)
