"""Minimal dependency-free validator for VCP/KF-POC-01.

The POC intentionally validates a narrow YAML subset using structural
checks rather than a third-party parser. It does not grant authority.
"""

from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
COMPONENT = ROOT / ".vanguard" / "component.yaml"
PATTERN = ROOT / "knowledge" / "patterns" / "vcp-kf-poc-01.yaml"


def read(path: Path) -> str:
    if not path.is_file():
        raise AssertionError(f"missing: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def require(text: str, pattern: str, label: str) -> None:
    if not re.search(pattern, text, re.MULTILINE):
        raise AssertionError(f"missing {label}")


def main() -> int:
    component = read(COMPONENT)
    knowledge = read(PATTERN)

    require(component, r"^component:$", "component root")
    require(component, r"^  id: vanguard-ai$", "component id")
    require(component, r"^contracts:$", "contracts")
    require(component, r"^knowledge:$", "knowledge declaration")
    require(component, r"^  evidence_required: true$", "evidence boundary")

    require(knowledge, r"^knowledge:$", "knowledge root")
    require(knowledge, r"^  schema: ["']v0\.1["']$", "knowledge schema")
    require(knowledge, r"^  status: hypothesis$", "hypothesis status")
    require(knowledge, r"^  promotion:$", "promotion gate")
    require(knowledge, r"^    verifier: VERITAS$", "VERITAS gate")

    print("VCP/KF-POC-01: PASS")
    print("knowledge: shareable")
    print("authority: not delegated")
    print("promotion: evidence-gated")
    return 0


if __name__ == "__main__":
    sys.exit(main())
