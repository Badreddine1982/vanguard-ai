import unittest

from vanguard.adapters.harness.base import ExecutionRequest, ExecutionResult, HarnessAdapter, PermissionContext
from vanguard.adapters.harness.deepseek import DeepSeekHarnessAdapter


class FakeRuntime:
    def __init__(self, supported=("code", "browser"), result=None, error=None):
        self.supported = frozenset(supported)
        self.result = result or ExecutionResult(ok=True, output="ok", runtime="fake")
        self.error = error
        self.last_request = None

    def capabilities(self):
        return self.supported

    def execute(self, request):
        self.last_request = request
        if self.error:
            raise self.error
        return self.result


class Audit:
    def __init__(self):
        self.events = []

    def emit(self, event):
        self.events.append(event)


class HarnessAdapterTests(unittest.TestCase):
    def test_permission_propagation(self):
        runtime, audit = FakeRuntime(), Audit()
        request = ExecutionRequest(
            task="inspect",
            capabilities=frozenset({"code"}),
            permission=PermissionContext(frozenset({"code"}), principal="test"),
        )
        result = HarnessAdapter(runtime, audit).execute(request)
        self.assertTrue(result.ok)
        self.assertEqual(runtime.last_request, request)
        self.assertEqual(audit.events[-1]["principal"], "test")

    def test_denial_without_granted_capability(self):
        result = HarnessAdapter(FakeRuntime()).execute(
            ExecutionRequest(task="x", capabilities=frozenset({"code"}))
        )
        self.assertFalse(result.ok)
        self.assertTrue(result.error.startswith("permission_denied:"))

    def test_unsupported_capability(self):
        result = HarnessAdapter(FakeRuntime(supported=("code",))).execute(
            ExecutionRequest(
                task="x",
                capabilities=frozenset({"browser"}),
                permission=PermissionContext(frozenset({"browser"})),
            )
        )
        self.assertFalse(result.ok)
        self.assertTrue(result.error.startswith("unsupported_capability:"))

    def test_success_and_audit_normalization(self):
        audit = Audit()
        adapter = DeepSeekHarnessAdapter(FakeRuntime(), audit)
        result = adapter.execute(
            ExecutionRequest(
                task="run",
                capabilities=frozenset({"code"}),
                permission=PermissionContext(frozenset({"code"})),
            )
        )
        self.assertTrue(result.ok)
        self.assertEqual(result.runtime, "fake")
        self.assertEqual(audit.events[-1]["runtime"], "deepseek-harness")

    def test_runtime_failure_is_normalized(self):
        result = HarnessAdapter(FakeRuntime(error=RuntimeError("boom"))).execute(
            ExecutionRequest(task="x")
        )
        self.assertFalse(result.ok)
        self.assertIn("runtime_error:RuntimeError:boom", result.error)


if __name__ == "__main__":
    unittest.main()
