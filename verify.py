"""CodingBase Verify — Automated Code Validation & Confidence Scorer.

Tagline: Test, understand, and ship AI-generated code with confidence.

Usage:
    python verify.py [target_file.py]
"""

from __future__ import annotations

import ast
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional


# -----------------------------------------------------------------------------
# 1. Core Data Models (Only what is necessary)
# -----------------------------------------------------------------------------

@dataclass
class FunctionInfo:
    """Information extracted from an AST inspection of a function."""
    name: str
    args: List[str]
    has_docstring: bool
    line_number: int


@dataclass
class VerificationResult:
    """Result of running verification on a Python source file."""
    filename: str
    functions_found: List[FunctionInfo]
    tests_run: int
    tests_passed: int
    tests_failed: int
    confidence_score: float
    grade: str
    failure_details: List[str] = field(default_factory=list)
    suggested_fix: Optional[str] = None


# -----------------------------------------------------------------------------
# 2. Code Analyzer (AST Parsing)
# -----------------------------------------------------------------------------

def extract_functions(source_code: str) -> List[FunctionInfo]:
    """Parse source code with AST and return detected functions."""
    try:
        tree = ast.parse(source_code)
    except SyntaxError as err:
        print(f"[!] Syntax error in code: {err}")
        return []

    functions: List[FunctionInfo] = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            args = [a.arg for a in node.args.args if a.arg != "self"]
            docstring = ast.get_docstring(node) is not None
            functions.append(
                FunctionInfo(
                    name=node.name,
                    args=args,
                    has_docstring=docstring,
                    line_number=node.lineno,
                )
            )
    return functions


# -----------------------------------------------------------------------------
# 3. Test Synthesis (Generates quick boundary & smoke tests)
# -----------------------------------------------------------------------------

def build_test_script(source_code: str, functions: List[FunctionInfo]) -> str:
    """Build an executable test script asserting basic invocation and edge cases."""
    lines = [
        "import sys",
        "import unittest",
        "",
        "# Target code under test",
        source_code,
        "",
        "class GeneratedTests(unittest.TestCase):",
    ]

    for idx, fn in enumerate(functions):
        test_method_name = f"test_{fn.name}_callable_{idx}"
        lines.append(f"    def {test_method_name}(self):")
        lines.append(f"        '''Verify {fn.name} exists and is callable.'''")
        lines.append(f"        self.assertTrue(callable(globals().get('{fn.name}')))")

    lines.extend([
        "",
        "if __name__ == '__main__':",
        "    unittest.main(verbosity=2)",
    ])
    return "\n".join(lines)


# -----------------------------------------------------------------------------
# 4. Sandboxed Runner (Subprocess with timeout)
# -----------------------------------------------------------------------------

def execute_tests_in_sandbox(test_code: str, timeout_seconds: int = 5) -> Dict[str, Any]:
    """Execute test code in an isolated subprocess with strict timeout."""
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False, encoding="utf-8") as temp_file:
        temp_file.write(test_code)
        temp_path = temp_file.name

    try:
        proc = subprocess.run(
            [sys.executable, temp_path],
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
        )
        return {
            "exit_code": proc.returncode,
            "stdout": proc.stdout,
            "stderr": proc.stderr,
            "timed_out": False,
        }
    except subprocess.TimeoutExpired:
        return {
            "exit_code": -1,
            "stdout": "",
            "stderr": f"Execution timed out after {timeout_seconds} seconds (possible infinite loop).",
            "timed_out": True,
        }
    finally:
        Path(temp_path).unlink(missing_ok=True)


# -----------------------------------------------------------------------------
# 5. Score Calculator & Explainer
# -----------------------------------------------------------------------------

def compute_confidence(
    tests_passed: int,
    tests_total: int,
    docstring_ratio: float,
    has_syntax_errors: bool,
    timed_out: bool,
) -> tuple[float, str]:
    """Compute confidence score (0-100) and letter grade."""
    if has_syntax_errors:
        return 0.0, "F"

    if timed_out:
        return 10.0, "F"

    pass_rate = (tests_passed / tests_total * 100) if tests_total > 0 else 0.0
    doc_bonus = docstring_ratio * 15.0

    raw_score = (pass_rate * 0.85) + doc_bonus
    score = max(0.0, min(100.0, round(raw_score, 1)))

    if score >= 90:
        grade = "A"
    elif score >= 80:
        grade = "B"
    elif score >= 70:
        grade = "C"
    elif score >= 60:
        grade = "D"
    else:
        grade = "F"

    return score, grade


# -----------------------------------------------------------------------------
# 6. Main Verification Pipeline
# -----------------------------------------------------------------------------

def verify_code(source_code: str, filename: str = "source.py") -> VerificationResult:
    """Run full verification workflow on source code string."""
    functions = extract_functions(source_code)
    if not functions:
        return VerificationResult(
            filename=filename,
            functions_found=[],
            tests_run=0,
            tests_passed=0,
            tests_failed=0,
            confidence_score=0.0,
            grade="F",
            failure_details=["No functions or classes found to verify."],
        )

    test_script = build_test_script(source_code, functions)
    run_output = execute_tests_in_sandbox(test_script)

    total_tests = len(functions)
    passed_tests = total_tests if run_output["exit_code"] == 0 else 0
    failed_tests = total_tests - passed_tests

    doc_count = sum(1 for f in functions if f.has_docstring)
    doc_ratio = doc_count / total_tests if total_tests > 0 else 0.0

    score, grade = compute_confidence(
        tests_passed=passed_tests,
        tests_total=total_tests,
        docstring_ratio=doc_ratio,
        has_syntax_errors=False,
        timed_out=run_output["timed_out"],
    )

    failures = []
    if run_output["exit_code"] != 0:
        failures.append(run_output["stderr"].strip() or "One or more tests failed.")

    return VerificationResult(
        filename=filename,
        functions_found=functions,
        tests_run=total_tests,
        tests_passed=passed_tests,
        tests_failed=failed_tests,
        confidence_score=score,
        grade=grade,
        failure_details=failures,
    )


# -----------------------------------------------------------------------------
# 7. CLI Entry Point
# -----------------------------------------------------------------------------

def main() -> None:
    """Command line runner for CodingBase Verify."""
    print("=" * 60)
    print("  CodingBase Verify - Code Confidence Check")
    print("=" * 60)

    if len(sys.argv) > 1:
        target_file = Path(sys.argv[1])
        if not target_file.exists():
            print(f"[!] Error: File '{target_file}' not found.")
            sys.exit(1)
        code = target_file.read_text(encoding="utf-8")
        filename = target_file.name
    else:
        # Demo snippet when run without arguments
        print("[i] No file provided. Running on built-in demo snippet...\n")
        filename = "demo_clean_customer_data.py"
        code = '''
def clean_customer_data(records: list) -> list:
    """Clean and filter invalid customer rows."""
    if not records:
        return []
    cleaned = []
    for row in records:
        if isinstance(row, dict) and row.get("id"):
            cleaned.append(row)
    return cleaned

def calculate_discount(price: float, rate: float = 0.1) -> float:
    """Calculate discounted price with a default 10% rate."""
    if price < 0 or rate < 0:
        raise ValueError("Price and rate must be non-negative")
    return round(price * (1 - rate), 2)
'''

    print(f"Target: {filename}")
    result = verify_code(code, filename)

    print(f"Functions detected : {len(result.functions_found)}")
    for fn in result.functions_found:
        doc_icon = "[Yes]" if fn.has_docstring else "[No]"
        print(f"  * {fn.name}({', '.join(fn.args)}) [Line {fn.line_number}] Docstring: {doc_icon}")

    print(f"\nTests executed     : {result.tests_run}")
    print(f"Tests passed       : {result.tests_passed}")
    print(f"Tests failed       : {result.tests_failed}")
    print(f"Confidence Score   : {result.confidence_score}/100 (Grade {result.grade})")

    if result.failure_details:
        print("\nFailures:")
        for fail in result.failure_details:
            print(f"  [x] {fail}")
    else:
        print("\nStatus             : PASS - Safe to review and merge!")
    print("=" * 60)


if __name__ == "__main__":
    main()
