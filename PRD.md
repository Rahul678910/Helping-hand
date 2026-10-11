# Product Requirements Document (PRD): CodingBase Verify

**Tagline:** Test, understand, and ship AI-generated code with confidence.  
**Version:** 1.0.0 (MVP)  
**Status:** In Progress  
**Source Document:** [IDEAS.md](file:///c:/Users/RAM/DAS/MURMU/OneDrive/Desktop/Helper/IDEAS.md)

---

## 1. Executive Summary & Vision

### 1.1 Product Vision
As AI code generators (GitHub Copilot, Cursor, ChatGPT, Claude) accelerate raw code production, the bottleneck in software development shifts from **writing code** to **verifying code**. AI-generated code frequently contains subtle logical flaws, missed edge cases, hallucinated APIs, and security vulnerabilities.

**CodingBase Verify** is an automated code validation, testing, and confidence platform. It ingests source code (or connects to repositories), analyzes code structure via AST, automatically synthesizes rigorous test suites (including boundary and edge cases), executes tests within an isolated sandbox, diagnoses failures in plain English, suggests targeted code fixes, and computes an objective **Code Confidence Score (0–100%)**.

---

## 2. Target Audience & Core Problems

### 2.1 Target Personas
- **Individual Developers:** Need immediate confirmation that AI-generated code actually works before copying it into their codebases.
- **Engineering Teams & Startups:** Need fast, automated pull-request validation to prevent regressions from AI-assisted commits.
- **Open-Source Maintainers:** Need automated test suites and confidence scores for incoming PRs from contributors.

### 2.2 Core Problems Solved
1. **Missed Edge Cases:** AI code assistants write "happy path" logic; edge cases (null inputs, type mismatch, large payloads) are overlooked.
2. **Test Generation Friction:** Developers dislike writing boilerplate unit tests manually.
3. **Cryptic Test Failures:** Stack traces can be obscure; developers waste hours debugging test failures.
4. **Lack of Merging Confidence:** No standard metric exists to quantify how trustworthy AI-generated code is before merging.

---

## 3. System Architecture & Tech Stack

```mermaid
flowchart TD
    User["Developer / Web UI / CLI"] -->|Uploads Code| Ingest["Code Ingestion & Validation"]
    Ingest --> AST["AST Parser Engine (Python ast / Babel)"]
    AST -->|Extracted Signatures, Types, Docs| TestGen["AI Test Synthesizer (LLM Prompt Engine)"]
    TestGen -->|Generates Unit Tests (pytest / Jest)| Sandbox["Secure Isolated Sandbox Runner"]
    Sandbox -->|Execution Traces & Coverage| OutputParser["Test Output & Coverage Parser"]
    OutputParser -->|Pass/Fail Diagnostics| Diagnostician["AI Failure Explainer & Fix Suggester"]
    OutputParser --> Scorer["Code Confidence Score Engine"]
    Diagnostician --> Results["Dashboard / JSON Report"]
    Scorer --> Results
```

### 3.1 Recommended Technology Stack
- **Backend API:** Python 3.11+ with FastAPI, Pydantic v2, and Uvicorn.
- **Frontend Dashboard:** Next.js (App Router), TypeScript, Tailwind CSS, Monaco Code Editor.
- **Code Parsing Engine:** Python `ast` / `tree-sitter` for multi-language AST extraction (Python, JavaScript/TypeScript).
- **Execution Sandbox:** Containerized / Process-isolated sandbox with memory limits (e.g., 256MB), strict execution timeouts (e.g., 5 seconds), and network isolation.
- **Test Frameworks Supported (MVP):** `pytest` for Python; `Jest` / `vitest` for JavaScript/TypeScript.
- **AI Engine:** Structured LLM calls (OpenAI / Anthropic / Gemini API) with JSON schemas for deterministic test and fix generation.

---

## 4. MVP Feature Specifications

### 4.1 Feature 1: Code Ingestion & AST Analysis
- Accepts raw code via direct paste or file upload (`.py`, `.js`, `.ts`).
- Parses code structure using AST:
  - Extracts module-level functions, class definitions, method signatures.
  - Identifies input parameters, type hints/annotations, and docstrings.
  - Detects external dependencies and internal imports.

### 4.2 Feature 2: Automated Unit Test Synthesis
- Synthesizes comprehensive unit tests targeting:
  - **Happy Path:** Normal inputs and standard use cases.
  - **Boundary Conditions:** Empty strings, zero, negative numbers, maximum integers, empty lists/dicts.
  - **Type & Exception Safety:** Invalid types, `None`/`null` handling, expected error raises.
- Outputs standardized test files (`test_module.py` or `module.test.js`).

### 4.3 Feature 3: Secure Isolated Sandbox Runner
- Mounts code and generated tests in a sandboxed execution environment.
- Enforces strict resource constraints:
  - Max runtime: 5 seconds per suite (kill on timeout to prevent infinite loops).
  - Max memory: 256 MB.
  - Network access disabled (`--network none`).
- Captures `stdout`, `stderr`, exit codes, and coverage metrics.

### 4.4 Feature 4: Plain-Language Diagnostics & Fix Generator
- If a test fails:
  - Identifies failing assertion and line number.
  - Translates technical stack traces into concise, human-friendly explanations.
  - Generates a targeted code patch (unified diff) to fix the bug without modifying unrelated logic.

### 4.5 Feature 5: Code Confidence Score Algorithm
A quantitative score from **0 to 100** calculated as:

$$\text{Confidence Score} = w_1 \cdot P + w_2 \cdot C + w_3 \cdot E + w_4 \cdot H - \text{Penalties}$$

Where:
- **$P$ (Pass Rate, 40%):** $\frac{\text{Passed Tests}}{\text{Total Tests}} \times 100$
- **$C$ (Branch/Line Coverage, 25%):** Percentage of code statements exercised by tests.
- **$E$ (Edge Case Resilience, 20%):** Proportion of boundary condition assertions passed.
- **$H$ (Complexity Health, 15%):** Cyclomatic complexity penalty scale ($100$ for simple code, scaled down for high complexity).
- **$\text{Penalties}$:** Deductions for unhandled exceptions (-10) or timeout/infinite loop risks (-25).

---

## 5. Granular Task Backlog (Ralph Loop Ready)

<!-- Tasks are ordered, discrete, and independently verifiable -->

### Phase 1: Project Scaffolding & Core Foundations
- [x] **Task 1: Project Initialization & Environment Setup**
  - Setup Python/FastAPI backend structure with pytest, ruff, and pre-commit configurations.
  - Setup requirements.txt and `.env.example`.
- [ ] **Task 2: AST Code Analysis Engine**
  - Implement AST parser for Python code (`ast` module) extracting function names, arguments, return annotations, and docstrings.
  - Add unit tests validating AST extraction for standard functions, classes, and edge-case syntax.

### Phase 2: Test Generation & Sandbox Execution
- [ ] **Task 3: Test Generation Prompt & Synthesis Engine**
  - Create prompt templates for test generation covering happy paths, boundary values, and exception tests.
  - Build mockable LLM service layer returning formatted test files.
- [ ] **Task 4: Sandboxed Test Runner**
  - Implement an isolated subprocess runner for `pytest` with timeout enforcement (5s) and stdout/stderr capture.
  - Add security checks preventing dangerous imports (e.g., `os.system`, `subprocess` in unverified code).
- [ ] **Task 5: Test Execution Report Parser**
  - Parse pytest XML/JSON output into structured results: total tests, passed, failed, errors, execution time.

### Phase 3: Diagnostics, Auto-Fixing & Confidence Scoring
- [ ] **Task 6: Failure Diagnostics & AI Fix Engine**
  - Build failure explanation service that ingests failing assertion tracebacks and generates plain-language explanations.
  - Generate a unified diff fix for the failing code.
- [ ] **Task 7: Code Confidence Score Calculator**
  - Implement the multi-factor scoring formula (Pass Rate, Coverage, Edge Cases, Complexity).
  - Return breakdown ratings (High/Medium/Low confidence) and actionable recommendations.

### Phase 4: API & User Interface
- [ ] **Task 8: REST API Endpoints**
  - Create `/api/verify` endpoint (upload/submit code, run full pipeline, return JSON report).
  - Create `/api/diagnose` and `/api/fix` endpoints.
- [ ] **Task 9: Interactive Web Dashboard / CLI**
  - Build clean web interface (or lightweight CLI) with Monaco/syntax-highlighted editor, pass/fail status pills, failure breakdowns, and confidence meter.
- [ ] **Task 10: End-to-End Verification & Documentation**
  - Write end-to-end integration tests using representative Python code samples (cleaning script, calculation utility, data transformer).
  - Finalize README.md with setup instructions and usage guide.
