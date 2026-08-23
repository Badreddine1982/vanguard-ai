import ast
from typing import Set


class SecurityValidator:
    """التحقق من أمان الكود قبل التنفيذ"""

    DANGEROUS_FUNCTIONS: Set[str] = {
        "exec", "eval", "compile", "__import__",
        "open", "file", "input", "raw_input",
        "system", "popen", "subprocess",
        "shutil", "os", "sys",
    }

    @classmethod
    def validate_code(cls, code: str) -> bool:
        """التحقق من أن الكود آمن للتنفيذ"""
        try:
            tree = ast.parse(code)
        except SyntaxError:
            return False

        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if cls._get_func_name(node) in cls.DANGEROUS_FUNCTIONS:
                    return False

            if isinstance(node, ast.Import):
                for name in node.names:
                    if name.name.split(".")[0] in cls.DANGEROUS_FUNCTIONS:
                        return False

            if isinstance(node, ast.ImportFrom):
                if node.module and node.module.split(".")[0] in cls.DANGEROUS_FUNCTIONS:
                    return False

        return True

    @classmethod
    def _get_func_name(cls, node: ast.Call) -> str:
        """استخراج اسم الدالة من عقدة AST"""
        if isinstance(node.func, ast.Name):
            return node.func.id
        if isinstance(node.func, ast.Attribute):
            return node.func.attr
        return ""

    @classmethod
    def sanitize_path(cls, path: str) -> str:
        """تنقية المسار من هجمات المسار النسبي"""
        if ".." in path:
            path = path.replace("..", "")

        dangerous_chars = [";", "|", "&", "$", "`", ">", "<", '"', "'"]
        for char in dangerous_chars:
            path = path.replace(char, "")

        return path
