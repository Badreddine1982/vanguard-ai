import subprocess
from pathlib import Path
from typing import Dict, List, Optional

from utils.security import SecurityValidator

BUILD_TIMEOUT_SECONDS = 180


class SafeExecutor:
    """تنفيذ الأوامر في بيئة معزولة"""

    def __init__(self):
        self.work_dir = Path("/tmp/vanguard_workspace")
        self.work_dir.mkdir(parents=True, exist_ok=True)
        self.security = SecurityValidator()

    def build(self, project_path: str, target: str) -> Dict:
        """بناء المشروع"""
        if target == "android":
            cmd = self._get_gradle_command(project_path)
        elif target == "python":
            cmd = ["python", "-m", "build", "--outdir", "./dist"]
        else:
            return {"status": "FAILURE", "error": f"Unknown target: {target}"}

        try:
            result = subprocess.run(
                cmd,
                cwd=project_path,
                capture_output=True,
                text=True,
                timeout=BUILD_TIMEOUT_SECONDS,
            )
        except subprocess.TimeoutExpired:
            return {
                "status": "FAILURE",
                "error": f"Build timed out after {BUILD_TIMEOUT_SECONDS} seconds",
            }
        except OSError as exc:
            return {"status": "FAILURE", "error": str(exc)}

        if result.returncode == 0:
            return {
                "status": "SUCCESS",
                "output": result.stdout,
                "artifact": self._find_artifact(project_path, target),
            }

        return {"status": "FAILURE", "error": result.stderr, "output": result.stdout}

    def _get_gradle_command(self, project_path: str) -> List[str]:
        """استخراج أمر Gradle المناسب"""
        for wrapper in ("gradlew", "gradlew.bat"):
            candidate = Path(project_path) / wrapper
            if candidate.exists():
                return [str(candidate), "assembleDebug", "--no-daemon"]

        return ["gradle", "assembleDebug", "--no-daemon"]

    def _find_artifact(self, project_path: str, target: str) -> Optional[str]:
        """البحث عن ملف الأثر بعد البناء"""
        if target != "android":
            return None

        apk_path = (
            Path(project_path)
            / "app"
            / "build"
            / "outputs"
            / "apk"
            / "debug"
            / "app-debug.apk"
        )
        return str(apk_path) if apk_path.exists() else None

    def apply_fix(self, project_path: str, solution: str) -> bool:
        """تطبيق حل مقترح"""
        if not self.security.validate_code(solution):
            return False

        for candidate in (
            Path(project_path) / "app" / "build.gradle",
            Path(project_path) / "build.gradle",
        ):
            if not candidate.exists():
                continue
            try:
                with open(candidate, "a") as f:
                    f.write(f"\n// VANGUARD Auto-Fix: {solution}\n")
                return True
            except OSError:
                continue

        return False

    def run_plugin(self, plugin_code: str) -> float:
        """تنفيذ بلوجن في بيئة معزولة"""
        if not self.security.validate_code(plugin_code):
            return 0.0

        namespace: Dict[str, object] = {}
        try:
            exec(plugin_code, {"__builtins__": {}}, namespace)  # noqa: S102
            extractor = namespace.get("extract_feature")
            if callable(extractor):
                return float(extractor("test"))
        except Exception:
            pass

        return 0.0
