"""Unit tests for verify.py."""

import unittest
from verify import (
    compute_confidence,
    extract_functions,
    verify_code,
)


class TestVerify(unittest.TestCase):
    def test_extract_functions(self):
        sample = '''
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b
'''
        funcs = extract_functions(sample)
        self.assertEqual(len(funcs), 1)
        self.assertEqual(funcs[0].name, "add")
        self.assertEqual(funcs[0].args, ["a", "b"])
        self.assertTrue(funcs[0].has_docstring)

    def test_compute_confidence_scoring(self):
        score, grade = compute_confidence(
            tests_passed=5,
            tests_total=5,
            docstring_ratio=1.0,
            has_syntax_errors=False,
            timed_out=False,
        )
        self.assertEqual(score, 100.0)
        self.assertEqual(grade, "A")

    def test_verify_code_valid(self):
        sample = '''
def multiply(x, y):
    """Multiply x by y."""
    return x * y
'''
        result = verify_code(sample, "math.py")
        self.assertEqual(result.tests_passed, 1)
        self.assertEqual(result.tests_failed, 0)
        self.assertGreaterEqual(result.confidence_score, 80.0)

    def test_verify_code_empty(self):
        result = verify_code("", "empty.py")
        self.assertEqual(result.tests_run, 0)
        self.assertEqual(result.grade, "F")


if __name__ == "__main__":
    unittest.main()
