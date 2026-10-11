# 🛡️ CodingBase Verify

<p align="center">
  <strong>Test, understand, and ship AI-generated code with confidence.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.10%2B-blue.svg" alt="Python 3.10+">
  <img src="https://img.shields.io/badge/tests-14%20passed-brightgreen.svg" alt="Tests">
  <img src="https://img.shields.io/badge/dependencies-0%20external-orange.svg" alt="Zero Dependencies">
  <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="License">
</p>

---

## 📌 Overview

AI coding assistants (Copilot, Cursor, ChatGPT, Claude) can write code in seconds, but developers still need confidence that generated code is correct, well-structured, and safe from regressions.

**CodingBase Verify** is a lightweight, automated code validation engine. It parses Python source code via AST, detects functions and parameters, runs test execution in an isolated sandbox with timeout guards, and computes an objective **Code Confidence Score (0–100%)**.

---

## ⚡ Quick Start (30 Seconds)

### 1. Clone the repository
```bash
git clone https://github.com/your-username/codingbase-verify.git
cd codingbase-verify
```

### 2. Write your code in `your_file.py`
Open [`your_file.py`](file:///c:/Users/RAM/DAS/MURMU/OneDrive/Desktop/Helper/your_file.py) and write or paste any Python functions you want to verify:

```python
# your_file.py

def calculate_discount(price: float, rate: float = 0.1) -> float:
    """Calculate the final discounted price."""
    if price < 0 or rate < 0:
        raise ValueError("Price and discount rate must be non-negative")
    return round(price * (1 - rate), 2)
```

### 3. Run Verification
```bash
python verify.py
```
*(Or specify any custom file: `python verify.py path/to/my_script.py`)*

---

## 🖥️ Example Output

```text
============================================================
  CodingBase Verify - Code Confidence Check
============================================================
[i] Verifying source file: your_file.py
    (Write your code in your_file.py, or run: python verify.py <file.py>)

Target: your_file.py
Functions detected : 3
  * clean_customer_data(records) [Line 11] Docstring: [Yes]
  * calculate_discount(price, rate) [Line 30] Docstring: [Yes]
  * validate_email_address(email) [Line 45] Docstring: [Yes]

Tests executed     : 3
Tests passed       : 3
Tests failed       : 0
Confidence Score   : 100.0/100 (Grade A)

Status             : PASS - Safe to review and merge!
============================================================
```

---

## ✨ Key Features

- 🔍 **AST Function & Signature Inspection:** Automatically extracts function signatures, argument lists, line numbers, and docstring coverage without executing unverified code.
- 🧪 **Sandboxed Subprocess Execution:** Executes synthesized tests in an isolated Python process with strict 5-second timeouts to guard against infinite loops or hangs.
- 📊 **Multi-Factor Code Confidence Score:** Quantifies code readiness from $0$ to $100\%$ using a weighted formula based on test pass rates, boundary resilience, and documentation health.
- ⚡ **Zero External Dependencies:** Built entirely with Python's standard library (`ast`, `subprocess`, `unittest`, `tempfile`). No heavy setup required.

---

## 🧮 Code Confidence Score Breakdown

The Confidence Score uses a weighted evaluation model:

| Metric | Weight | Description |
| :--- | :---: | :--- |
| **Test Pass Rate** | **85%** | Percentage of generated boundary and callable tests that succeed. |
| **Docstring Health** | **15%** | Ratio of functions equipped with clear documentation / type specs. |
| **Timeout / Loop Penalties** | **-90%** | Critical deduction if execution hangs or exceeds timeout limits. |
| **Syntax Errors** | **0% (Grade F)** | Immediate score drop to 0 if code cannot be parsed by AST. |

### Letter Grades

| Score Range | Grade | Recommendation |
| :---: | :---: | :--- |
| **90 – 100** | **A** | **High Confidence:** Safe to review and merge into production. |
| **80 – 89** | **B** | **Good Confidence:** Minor improvements or test additions recommended. |
| **70 – 79** | **C** | **Moderate:** Missing docstrings or untested branches detected. |
| **60 – 69** | **D** | **Low:** Several checks failed; revision needed before merging. |
| **< 60** | **F** | **Critical:** Unhandled exceptions, timeouts, or syntax errors present. |

---

## 📁 Repository Structure

```text
├── your_file.py          # The source file: write or paste your Python code here!
├── verify.py             # CLI verification tool (AST parser, sandbox runner, scorer)
├── codingbase/           # Core package models & scoring algorithms
│   └── __init__.py       # Pydantic/dataclass models & compute_confidence_score()
├── tests/                # Comprehensive unit test suite
│   ├── test_init.py      # Tests for core models and score calculations
│   └── test_verify.py    # Tests for verify.py AST extraction and execution
├── PRD.md                # Product Requirements Document & development roadmap
├── IDEAS.md              # Original Top 5 market ideas analysis
├── progress.txt          # Ralph Loop development journal
├── pyproject.toml        # Package configuration
└── README.md             # This documentation
```

---

## 🧪 Running the Test Suite

Run all unit tests using Python's built-in `unittest`:

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

Or using `uv`:

```bash
uv run python -m unittest discover -s tests -p "test_*.py" -v
```

---

## 🗺️ Product Roadmap

CodingBase Verify is the first module in the CodingBase ecosystem. Next milestones from [`PRD.md`](file:///c:/Users/RAM/DAS/MURMU/OneDrive/Desktop/Helper/PRD.md):

- [x] **Phase 1:** AST parsing, sandboxed execution, and confidence scoring.
- [ ] **Phase 2:** LLM prompt synthesizer for automatic pytest test generation.
- [ ] **Phase 3:** Automated plain-English failure diagnosis and git-diff auto-fixing.
- [ ] **Phase 4:** GitHub Actions CI/CD integration for automated Pull Request checks.

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.
