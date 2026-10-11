# CodingBase — Development Workspace

> **Tagline:** Test, understand, and ship AI-generated code with confidence.

Welcome to the **CodingBase** project repository. This workspace contains the product strategy, technical specifications, and development roadmap to build the first product: **CodingBase Verify**.

---

## 📁 Repository Overview

| File | Purpose |
| :--- | :--- |
| **[`verify.py`](file:///c:/Users/RAM/DAS/MURMU/OneDrive/Desktop/Helper/verify.py)** | Standalone, lightweight code verification CLI tool that inspects functions via AST, runs sandboxed tests, and outputs Code Confidence Scores. |
| **[`IDEAS.md`](file:///c:/Users/RAM/DAS/MURMU/OneDrive/Desktop/Helper/IDEAS.md)** | The original strategic market analysis featuring the Top 5 product concepts (Verify, Review, Learn, Docs, Secure) and the rationale for starting with Verify. |
| **[`PRD.md`](file:///c:/Users/RAM/DAS/MURMU/OneDrive/Desktop/Helper/PRD.md)** | The comprehensive **Product Requirements Document** for **CodingBase Verify (MVP)**, including system architecture, AST parsing specs, sandboxing security model, Code Confidence Score formula, and a 10-step granular task backlog. |
| **[`progress.txt`](file:///c:/Users/RAM/DAS/MURMU/OneDrive/Desktop/Helper/progress.txt)** | The append-only **Ralph Loop** development journal tracking execution history, technical decisions, test verification, and next actions. |

---

## 🎯 Recommended Next Step: Building CodingBase Verify (MVP)

The product backlog in [`PRD.md`](file:///c:/Users/RAM/DAS/MURMU/OneDrive/Desktop/Helper/PRD.md) is structured into 10 granular tasks:

1. **Task 1:** Project Initialization & Environment Setup
2. **Task 2:** AST Code Analysis Engine (function & signature extractor)
3. **Task 3:** Test Generation Prompt & Synthesis Engine
4. **Task 4:** Sandboxed Test Runner (isolated pytest execution with timeout guards)
5. **Task 5:** Test Execution Report Parser
6. **Task 6:** Failure Diagnostics & AI Fix Engine
7. **Task 7:** Code Confidence Score Calculator
8. **Task 8:** REST API Endpoints (FastAPI)
9. **Task 9:** Web Dashboard / CLI Interface
10. **Task 10:** End-to-End Verification & Real-world Demos

---

## 🚀 How to Execute

You can work through tasks step-by-step:
- **Interactive Development:** Prompt your assistant: *"Start Task 1: Setup project structure and configuration"*.
- **Autonomous Loop:** Run with the Ralph Loop workflow or slash command `/goal` to implement the roadmap incrementally with automated verification and logging.
