"""Unit tests for codingbase initialization, data structures, and scoring."""

import unittest
from codingbase import (
    CodeLanguage,
    CodeSnippet,
    ConfidenceScore,
    FunctionSignature,
    SingleTestResult,
    TestCategory,
    TestCase,
    TestStatus,
    VerificationReport,
    __tagline__,
    __title__,
    __version__,
    calculate_grade,
    compute_confidence_score,
    get_info,
)


class TestCodingBaseInit(unittest.TestCase):
    def test_metadata(self):
        self.assertEqual(__version__, "0.1.0")
        self.assertIn("Verify", __title__)
        self.assertTrue(len(__tagline__) > 0)
        info = get_info()
        self.assertEqual(info["version"], "0.1.0")
        self.assertEqual(info["title"], "CodingBase Verify")

    def test_enums(self):
        self.assertEqual(CodeLanguage.PYTHON.value, "python")
        self.assertEqual(CodeLanguage.JAVASCRIPT.value, "javascript")
        self.assertEqual(TestStatus.PASSED.value, "passed")
        self.assertEqual(TestStatus.FAILED.value, "failed")
        self.assertEqual(TestCategory.HAPPY_PATH.value, "happy_path")
        self.assertEqual(TestCategory.BOUNDARY.value, "boundary")

    def test_code_snippet_model(self):
        snippet = CodeSnippet(
            content="def add(a, b): return a + b",
            language=CodeLanguage.PYTHON,
            filename="math_util.py",
        )
        self.assertEqual(snippet.language, CodeLanguage.PYTHON)
        self.assertEqual(snippet.filename, "math_util.py")

    def test_function_signature_model(self):
        sig = FunctionSignature(
            name="clean_data",
            args=["df", "drop_duplicates"],
            return_type="DataFrame",
            docstring="Cleans customer tabular data.",
            line_start=10,
            line_end=25,
        )
        self.assertEqual(sig.name, "clean_data")
        self.assertEqual(len(sig.args), 2)
        self.assertEqual(sig.line_start, 10)

    def test_test_case_and_result_models(self):
        tc = TestCase(
            name="test_clean_data_nulls",
            code="def test_clean_data_nulls(): assert True",
            category=TestCategory.BOUNDARY,
            description="Test null values handling",
        )
        self.assertEqual(tc.category, TestCategory.BOUNDARY)

        result = SingleTestResult(
            test_name="test_clean_data_nulls",
            status=TestStatus.PASSED,
            duration_ms=12.4,
        )
        self.assertEqual(result.status, TestStatus.PASSED)
        self.assertEqual(result.duration_ms, 12.4)

    def test_confidence_score_perfect(self):
        score = compute_confidence_score(
            pass_rate=100.0,
            coverage_pct=100.0,
            edge_case_score=100.0,
            complexity_health=100.0,
        )
        self.assertEqual(score.score, 100.0)
        self.assertEqual(score.grade, "A")

    def test_confidence_score_weighted(self):
        # 0.4*100 (40) + 0.25*80 (20) + 0.20*50 (10) + 0.15*60 (9) = 79.0 -> grade C
        score = compute_confidence_score(
            pass_rate=100.0,
            coverage_pct=80.0,
            edge_case_score=50.0,
            complexity_health=60.0,
        )
        self.assertEqual(score.score, 79.0)
        self.assertEqual(score.grade, "C")

    def test_confidence_score_penalties_and_clamping(self):
        # Penalties exceed raw score -> clamps to 0.0
        score = compute_confidence_score(
            pass_rate=10.0,
            coverage_pct=10.0,
            edge_case_score=0.0,
            complexity_health=10.0,
            penalties=50.0,
        )
        self.assertEqual(score.score, 0.0)
        self.assertEqual(score.grade, "F")

    def test_grades(self):
        self.assertEqual(calculate_grade(95.0), "A")
        self.assertEqual(calculate_grade(85.0), "B")
        self.assertEqual(calculate_grade(75.0), "C")
        self.assertEqual(calculate_grade(65.0), "D")
        self.assertEqual(calculate_grade(45.0), "F")

    def test_verification_report(self):
        snippet = CodeSnippet(content="def foo(): pass")
        report = VerificationReport(
            snippet=snippet,
            functions_found=[FunctionSignature(name="foo")],
            tests_generated=[],
            results=[],
            confidence=compute_confidence_score(100, 100, 100, 100),
            explanation="All checks passed.",
        )
        self.assertEqual(report.explanation, "All checks passed.")
        self.assertIsNotNone(report.confidence)
        self.assertEqual(report.confidence.grade, "A")


if __name__ == "__main__":
    unittest.main()
