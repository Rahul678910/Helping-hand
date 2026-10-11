"""CodingBase Verify.

Test, understand, and ship AI-generated code with confidence.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional

__version__ = "0.1.0"
__title__ = "CodingBase Verify"
__tagline__ = "Test, understand, and ship AI-generated code with confidence."


class CodeLanguage(str, Enum):
    """Supported source code languages."""
    PYTHON = "python"
    JAVASCRIPT = "javascript"
    TYPESCRIPT = "typescript"


class TestStatus(str, Enum):
    """Execution status of a single unit test."""
    PASSED = "passed"
    FAILED = "failed"
    ERROR = "error"
    SKIPPED = "skipped"


class TestCategory(str, Enum):
    """Categorization for synthesized test cases."""
    HAPPY_PATH = "happy_path"
    BOUNDARY = "boundary"
    EXCEPTION = "exception"
    REGRESSION = "regression"


@dataclass
class CodeSnippet:
    """Represents ingested source code ready for validation."""
    content: str
    language: CodeLanguage = CodeLanguage.PYTHON
    filename: Optional[str] = None

    def __post_init__(self) -> None:
        if isinstance(self.language, str) and not isinstance(self.language, CodeLanguage):
            self.language = CodeLanguage(self.language.lower())


@dataclass
class FunctionSignature:
    """Extracted metadata for a function or method from AST analysis."""
    name: str
    args: List[str] = field(default_factory=list)
    return_type: Optional[str] = None
    docstring: Optional[str] = None
    line_start: int = 1
    line_end: int = 1


@dataclass
class TestCase:
    """Synthesized unit test case."""
    name: str
    code: str
    category: TestCategory = TestCategory.HAPPY_PATH
    description: str = ""

    def __post_init__(self) -> None:
        if isinstance(self.category, str) and not isinstance(self.category, TestCategory):
            self.category = TestCategory(self.category.lower())


@dataclass
class SingleTestResult:
    """Outcome from running an individual test."""
    test_name: str
    status: TestStatus
    duration_ms: float = 0.0
    error_message: Optional[str] = None
    traceback: Optional[str] = None

    def __post_init__(self) -> None:
        if isinstance(self.status, str) and not isinstance(self.status, TestStatus):
            self.status = TestStatus(self.status.lower())


@dataclass
class ConfidenceScore:
    """Quantified confidence metric for validated code."""
    score: float
    pass_rate: float
    coverage_pct: float
    edge_case_score: float
    complexity_health: float
    grade: str
    breakdown: Dict[str, Any] = field(default_factory=dict)


@dataclass
class VerificationReport:
    """Comprehensive verification output for a code snippet."""
    snippet: CodeSnippet
    functions_found: List[FunctionSignature] = field(default_factory=list)
    tests_generated: List[TestCase] = field(default_factory=list)
    results: List[SingleTestResult] = field(default_factory=list)
    confidence: Optional[ConfidenceScore] = None
    explanation: Optional[str] = None
    suggested_fix: Optional[str] = None


def calculate_grade(score: float) -> str:
    """Return letter grade rating based on confidence score."""
    if score >= 90.0:
        return "A"
    if score >= 80.0:
        return "B"
    if score >= 70.0:
        return "C"
    if score >= 60.0:
        return "D"
    return "F"


def compute_confidence_score(
    pass_rate: float,
    coverage_pct: float,
    edge_case_score: float,
    complexity_health: float,
    penalties: float = 0.0,
) -> ConfidenceScore:
    """Calculate the Code Confidence Score (0-100) per the PRD specification.

    Formula:
        Score = 0.40 * PassRate + 0.25 * Coverage + 0.20 * EdgeCases + 0.15 * ComplexityHealth - Penalties
    """
    raw_score = (
        (0.40 * pass_rate)
        + (0.25 * coverage_pct)
        + (0.20 * edge_case_score)
        + (0.15 * complexity_health)
        - penalties
    )
    clamped_score = max(0.0, min(100.0, round(raw_score, 2)))
    grade = calculate_grade(clamped_score)

    return ConfidenceScore(
        score=clamped_score,
        pass_rate=round(pass_rate, 2),
        coverage_pct=round(coverage_pct, 2),
        edge_case_score=round(edge_case_score, 2),
        complexity_health=round(complexity_health, 2),
        grade=grade,
        breakdown={
            "pass_rate_weight": 0.40,
            "coverage_weight": 0.25,
            "edge_case_weight": 0.20,
            "complexity_health_weight": 0.15,
            "penalties_applied": penalties,
        },
    )


def get_info() -> Dict[str, str]:
    """Return package metadata summary."""
    return {
        "title": __title__,
        "version": __version__,
        "tagline": __tagline__,
    }


__all__ = [
    "__version__",
    "__title__",
    "__tagline__",
    "CodeLanguage",
    "TestStatus",
    "TestCategory",
    "CodeSnippet",
    "FunctionSignature",
    "TestCase",
    "SingleTestResult",
    "ConfidenceScore",
    "VerificationReport",
    "calculate_grade",
    "compute_confidence_score",
    "get_info",
]
