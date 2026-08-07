import pytest
import torch

from agent.intelligence import VanguardIntelligence
from agent.models.router import AdaptiveRouter
from agent.orchestrator import VanguardOrchestrator


class TestVanguardAgent:
    def setup_method(self):
        self.orchestrator = VanguardOrchestrator()
        self.intelligence = VanguardIntelligence()

    def test_router_creation(self):
        """اختبار إنشاء الموجه العصبي"""
        router = AdaptiveRouter(input_dim=10, output_dim=3)
        assert router.input_dim == 10
        assert router.output_dim == 3

    def test_router_forward(self):
        """اختبار المرور الأمامي للشبكة"""
        router = AdaptiveRouter(input_dim=10, output_dim=3)
        output = router.forward(torch.randn(1, 10))
        assert output.shape == (1, 3)
        assert torch.allclose(output.sum(dim=1), torch.tensor([1.0]))

    def test_router_expand_input(self):
        """اختبار توسيع أبعاد الشبكة"""
        router = AdaptiveRouter(input_dim=10, output_dim=3)
        router.expand_input(12)
        assert router.input_dim == 12
        assert router.forward(torch.randn(1, 12)).shape == (1, 3)

    def test_feature_extraction(self):
        """اختبار استخراج الميزات"""
        code = "def hello():\n    print('Hello')\n\nfor i in range(10):\n    print(i)\n"
        features = self.intelligence.extract_features(code)
        assert features["functions"] > 0
        assert features["loops"] > 0
        assert features["lines"] > 0

    def test_feature_extraction_invalid_code(self):
        """اختبار استخراج الميزات من كود غير صالح"""
        features = self.intelligence.extract_features("def broken(:")
        assert features["has_errors"] == 1.0

    def test_analyze_function(self):
        """اختبار وظيفة التحليل"""
        result = self.orchestrator.analyze("./test_project")
        assert "features" in result
        assert "decision" in result
        assert "confidence" in result

    def test_build_unknown_target(self):
        """اختبار البناء بهدف غير معروف"""
        result = self.orchestrator.executor.build(".", "solaris")
        assert result["status"] == "FAILURE"

    def test_diagnose_returns_fallback_solution(self):
        """اختبار التشخيص عند غياب الذاكرة"""
        solutions = self.orchestrator.diagnose("unknown gradle error", "./")
        assert solutions
        assert solutions[0]["solution"]

    def test_memory_search(self):
        """اختبار البحث في الذاكرة"""
        results = self.orchestrator.memory.search_by_error("gradle build failed")
        assert isinstance(results, list)

    def test_learn_from_feedback(self):
        """اختبار التعلم من التغذية الراجعة"""
        features = self.intelligence.extract_features("x = 1\n")
        context = self.intelligence.get_system_context()
        loss = self.orchestrator.learn_from_feedback(features, context, 1)
        assert loss > 0

    def test_health_check(self):
        """اختبار فحص صحة النظام"""
        health = self.orchestrator.health_check()
        assert health["status"] == "operational"
        assert "stats" in health


if __name__ == "__main__":
    pytest.main(["-v"])
