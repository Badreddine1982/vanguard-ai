import ast
import os
from typing import Dict, Tuple

import psutil
import torch

from agent.memory import MemorySystem
from agent.models.router import AdaptiveRouter

FEATURE_KEYS = [
    "complexity",
    "functions",
    "loops",
    "try_except",
    "lines",
    "comments",
    "has_classes",
]

DECISION_PATHS = ["M1 (Accurate)", "M2 (Balanced)", "M3 (Fast)"]


class VanguardIntelligence:
    """الوعي والذكاء المركزي للنظام"""

    def __init__(self):
        self.router = AdaptiveRouter(input_dim=10, output_dim=3)
        self.memory = MemorySystem()
        self.llm_client = self._init_llm()

    def _init_llm(self):
        """تهيئة عميل LLM (Gemini أو OpenAI)"""
        api_key = os.getenv("VANGUARD_LLM_API_KEY")
        model = os.getenv("VANGUARD_LLM_MODEL", "gemini-pro")
        mock = os.getenv("VANGUARD_MOCK_LLM", "true").lower() == "true"

        if mock or not api_key:
            return None

        try:
            if "gemini" in model:
                import google.generativeai as genai

                genai.configure(api_key=api_key)
                return genai.GenerativeModel(model)

            from openai import OpenAI

            return OpenAI(api_key=api_key)
        except Exception:
            return None

    def extract_features(self, code: str) -> Dict[str, float]:
        """استخراج ميزات حقيقية من الكود باستخدام AST"""
        try:
            tree = ast.parse(code)
        except SyntaxError:
            return {
                "complexity": 0.0,
                "functions": 0.0,
                "loops": 0.0,
                "try_except": 0.0,
                "lines": min(len(code) / 5000, 1.0),
                "comments": 0.0,
                "has_classes": 0.0,
                "has_imports": 0.0,
                "has_gradle": 1.0 if "gradle" in code.lower() else 0.0,
                "has_errors": 1.0,
            }

        nodes = list(ast.walk(tree))
        num_funcs = sum(1 for n in nodes if isinstance(n, ast.FunctionDef))
        num_loops = sum(1 for n in nodes if isinstance(n, (ast.For, ast.While)))
        num_try = sum(1 for n in nodes if isinstance(n, ast.Try))
        num_classes = sum(1 for n in nodes if isinstance(n, ast.ClassDef))
        num_imports = sum(1 for n in nodes if isinstance(n, (ast.Import, ast.ImportFrom)))
        num_ifs = sum(1 for n in nodes if isinstance(n, ast.If))
        num_comments = sum(
            1 for line in code.split("\n") if line.strip().startswith("#")
        )

        complexity = 1 + num_loops + num_try + num_ifs

        return {
            "complexity": min(complexity / 10, 1.0),
            "functions": min(num_funcs / 5, 1.0),
            "loops": min(num_loops / 5, 1.0),
            "try_except": min(num_try / 3, 1.0),
            "lines": min(len(code) / 5000, 1.0),
            "comments": min(num_comments / 20, 1.0),
            "has_classes": min(num_classes / 3, 1.0),
            "has_imports": min(num_imports / 5, 1.0),
            "has_gradle": 1.0 if "gradle" in code.lower() else 0.0,
            "has_errors": 0.0,
        }

    def get_system_context(self) -> Dict[str, float]:
        """الحصول على سياق النظام الحالي"""
        try:
            cpu = psutil.cpu_percent() / 100
            memory = psutil.virtual_memory().percent / 100
            disk = psutil.disk_usage("/").percent / 100
        except Exception:
            cpu, memory, disk = 0.5, 0.5, 0.5

        return {"cpu": cpu, "memory": memory, "disk": disk, "priority": 0.5}

    def decide(self, features: Dict[str, float], context: Dict[str, float]) -> Tuple[str, float]:
        """اتخاذ القرار باستخدام الشبكة العصبية"""
        vector = self._features_to_vector(features, context)
        idx, confidence = self.router.predict(vector)
        return DECISION_PATHS[idx], confidence

    def learn_from_feedback(self, features: Dict, context: Dict, correct_path: int) -> float:
        """التعلم من النتائج السابقة"""
        vector = self._features_to_vector(features, context)
        return self.router.train_step(vector, correct_path)

    def ask_llm(self, prompt: str) -> str:
        """طلب المساعدة من LLM"""
        if self.llm_client is None:
            return "Suggestion: Check your build.gradle configuration."

        try:
            if hasattr(self.llm_client, "generate_content"):
                return self.llm_client.generate_content(prompt).text

            response = self.llm_client.chat.completions.create(
                model=os.getenv("VANGUARD_LLM_MODEL", "gpt-4o-mini"),
                messages=[{"role": "user", "content": prompt}],
            )
            return response.choices[0].message.content or ""
        except Exception:
            return "LLM request failed. Using fallback solution."

    def _features_to_vector(self, features: Dict, context: Dict) -> torch.Tensor:
        """تحويل الميزات والسياق إلى متجه موحد"""
        values = [float(features.get(key, 0.0)) for key in FEATURE_KEYS]
        values += [
            float(context.get("cpu", 0.5)),
            float(context.get("memory", 0.5)),
            float(context.get("priority", 0.5)),
        ]
        return torch.tensor([values], dtype=torch.float32)
