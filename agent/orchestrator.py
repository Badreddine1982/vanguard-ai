from pathlib import Path
from typing import Dict, List, Optional

from agent.executor import SafeExecutor
from agent.intelligence import VanguardIntelligence
from agent.memory import MemorySystem

VECTOR_KEYS = ["complexity", "functions", "loops", "try_except", "lines"]

READABLE_EXTENSIONS = [".py", ".java", ".kt", ".gradle", ".xml", ".json"]


class VanguardOrchestrator:
    """المنسق الرئيسي - العقل المدبر للنظام"""

    VERSION = "1.0.0"

    def __init__(self):
        self.intelligence = VanguardIntelligence()
        self.memory = MemorySystem()
        self.executor = SafeExecutor()
        self.stats = {
            "total_analyzes": 0,
            "total_builds": 0,
            "successful_builds": 0,
            "failed_builds": 0,
            "learned_solutions": 0,
        }

    def analyze(self, project_path: str, code_content: Optional[str] = None) -> Dict:
        """تحليل مشروع برمجي"""
        self.stats["total_analyzes"] += 1

        if not code_content:
            code_content = self._read_project_files(project_path)

        features = self.intelligence.extract_features(code_content)
        context = self.intelligence.get_system_context()
        decision, confidence = self.intelligence.decide(features, context)

        similar_solutions = self.memory.search_similar(self._to_vector(features))

        return {
            "features": features,
            "decision": decision,
            "confidence": confidence,
            "similar_solutions": similar_solutions,
            "context": context,
            "stats": self.stats,
        }

    def build(self, project_path: str, target: str) -> Dict:
        """بناء المشروع مع تصحيح ذاتي"""
        self.stats["total_builds"] += 1

        result = self.executor.build(project_path, target)
        if result["status"] == "SUCCESS":
            self.stats["successful_builds"] += 1
            return result

        self.stats["failed_builds"] += 1
        error = result.get("error") or "Unknown error"

        similar_cases = self.memory.search_by_error(error, top_k=3)
        if similar_cases:
            best_solution = similar_cases[0]
            if self.executor.apply_fix(project_path, best_solution["solution"]):
                final_result = self.executor.build(project_path, target)

                self.memory.record_outcome(
                    best_solution["id"],
                    success=(final_result["status"] == "SUCCESS"),
                )
                self._record_retry_outcome(final_result)
                return final_result

        llm_prompt = (
            f"Build error: {error}\n"
            f"Project: {project_path}\n"
            f"Target: {target}\n\n"
            "Suggest a specific fix for this error. "
            "Be concise and provide only the solution."
        )
        llm_solution = self.intelligence.ask_llm(llm_prompt)
        self.executor.apply_fix(project_path, llm_solution)

        features = self._extract_features_from_path(project_path)
        self.memory.store(
            error,
            llm_solution,
            {"project": project_path},
            self._to_vector(features),
        )
        self.stats["learned_solutions"] += 1

        final_result = self.executor.build(project_path, target)
        self._record_retry_outcome(final_result)

        return final_result

    def diagnose(
        self,
        error: str,
        project_path: str,
        code_context: Optional[str] = None,
    ) -> List[Dict]:
        """تشخيص خطأ واقتراح حلول"""
        results = self.memory.search_by_error(error, top_k=5)

        if len(results) < 3:
            prompt = (
                "Diagnose this build error and suggest specific fixes:\n\n"
                f"Error: {error}\n"
                f"Project: {project_path}\n"
                f"Context: {code_context or 'No additional context'}\n\n"
                "Provide 3 specific solutions."
            )
            response = self.intelligence.ask_llm(prompt)
            parsed = self._parse_llm_solutions(response)
            if not parsed and response.strip():
                parsed = [
                    {
                        "id": "llm-0",
                        "solution": response.strip(),
                        "similarity": 0.5,
                        "from_llm": True,
                    }
                ]
            results.extend(parsed)

        return results

    def learn_from_feedback(self, features: Dict, context: Dict, correct_path: int) -> float:
        """التعلم من نتائج سابقة"""
        return self.intelligence.learn_from_feedback(features, context, correct_path)

    def health_check(self) -> Dict:
        """فحص صحة النظام"""
        return {
            "status": "operational",
            "agent": "VANGUARD Pro",
            "version": self.VERSION,
            "stats": self.stats,
        }

    def _record_retry_outcome(self, result: Dict):
        """تحديث الإحصائيات بعد إعادة المحاولة"""
        if result["status"] != "SUCCESS":
            return
        self.stats["successful_builds"] += 1
        self.stats["failed_builds"] -= 1

    @staticmethod
    def _to_vector(features: Dict) -> List[float]:
        return [float(features.get(key, 0.0)) for key in VECTOR_KEYS]

    def _read_project_files(self, path: str) -> str:
        """قراءة ملفات المشروع"""
        path_obj = Path(path)
        if not path_obj.exists():
            return ""

        content = []
        for ext in READABLE_EXTENSIONS:
            for file in path_obj.rglob(f"*{ext}"):
                try:
                    with open(file, "r") as f:
                        content.append(f"# {file.name}\n{f.read()[:1000]}")
                except OSError:
                    continue

        return "\n\n".join(content[:5])

    def _extract_features_from_path(self, path: str) -> Dict:
        """استخراج ميزات من مسار مشروع"""
        return self.intelligence.extract_features(self._read_project_files(path))

    def _parse_llm_solutions(self, response: str) -> List[Dict]:
        """تحليل استجابة LLM إلى حلول مقترحة"""
        solutions = []

        for i, raw_line in enumerate(response.split("\n")):
            line = raw_line.strip()
            if line[:2] in ("1.", "2.", "3."):
                solutions.append(
                    {
                        "id": f"llm-{i}",
                        "solution": line[2:].strip(),
                        "similarity": 0.5,
                        "from_llm": True,
                    }
                )

        return solutions
