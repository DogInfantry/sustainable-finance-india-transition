# Contributing to Sustainable Finance — India Transition

Thank you for your interest in contributing. This repository is focused on **original, practitioner-grade research** on India's sustainable finance transition. Every contribution should be rigorous, well-cited, and India-specific.

---

## Table of Contents

- [Who Should Contribute](#who-should-contribute)
- [Development Setup](#development-setup)
- [Branch Naming](#branch-naming)
- [What We Welcome](#what-we-welcome)
- [What Is Out of Scope](#what-is-out-of-scope)
- [Pull Request Checklist](#pull-request-checklist)
- [Data Contribution Standards](#data-contribution-standards)
- [Model & Code Standards](#model--code-standards)
- [Reporting Issues](#reporting-issues)
- [Code of Conduct](#code-of-conduct)

---

## Who Should Contribute

This repo is built for:
- Finance practitioners (IB, PE, asset management, banking)
- Climate/ESG researchers and analysts
- Policy analysts working on SEBI/RBI frameworks
- Data scientists applying quantitative methods to Indian capital markets

All skill levels are welcome — see **Good First Issues** for entry points.

---

## Development Setup

```bash
# 1. Fork and clone
git clone https://github.com/<your-username>/sustainable-finance-india-transition.git
cd sustainable-finance-india-transition

# 2. Create a virtual environment (Python 3.10+)
python -m venv .venv
source .venv/bin/activate          # Linux/macOS
.venv\Scripts\activate             # Windows

# 3. Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt   # linting + testing tools

# 4. Verify setup
pytest tests/ -v
```

> **Python version:** 3.10 or higher is required.

---

## Branch Naming

Use lowercase, hyphenated names with a category prefix:

| Type | Pattern | Example |
|------|---------|----------|
| New feature / model | `feature/<short-desc>` | `feature/esg-credit-spread-model` |
| Data addition | `data/<dataset-name>` | `data/green-bonds-2024-update` |
| Bug fix | `fix/<issue-or-desc>` | `fix/climate-var-negative-weights` |
| Research / analysis | `research/<topic>` | `research/municipal-green-bonds` |
| Documentation | `docs/<what>` | `docs/brsr-core-methodology` |
| Notebook | `notebook/<topic>` | `notebook/sovereign-green-bond-analysis` |

Always branch from `main` unless a maintainer specifies otherwise.

---

## What We Welcome

### 🟢 High Priority
- **Data updates** — SEBI green bond registry updates, RBI circular additions, BRSR filing data
- **Missing models** — see open issues tagged `model-needed`
- **Sector expansion** — chemicals/fertilizers, aluminium, aviation, shipping
- **Notebook additions** — end-to-end analyses using existing `src/` modules
- **Policy analysis** — BRSR Core vs. BRSR Comprehensive, SGrB tranche analysis

### 🟡 Welcome
- ESG scoring methodology improvements
- Scenario parameter updates (IEA, NITI Aayog releases)
- CLI or API wrappers for existing models
- Improved documentation and methodology notes
- International comparisons (EU Taxonomy, ISSB alignment)

---

## What Is Out of Scope

- Non-India market coverage (outside of explicit India-comparison context)
- Investment advice or trading signals
- Proprietary/licensed data that cannot be redistributed
- Models without cited methodology or data sources
- Generic ESG tooling not grounded in Indian regulatory context

---

## Pull Request Checklist

Before submitting, confirm all of the following:

**Code**
- [ ] Code passes `pytest tests/` with no failures
- [ ] Passes `flake8 src/ tests/` (max line length 100)
- [ ] New functions include docstrings with parameters and return types
- [ ] Type hints used throughout

**Data**
- [ ] Source is cited inline (URL, document, or registry reference)
- [ ] No proprietary or licensed data committed to the repo
- [ ] Schema documented in relevant `data/README.md`
- [ ] Synthetic/illustrative data is clearly labelled as such

**Models**
- [ ] Methodology note added in `docs/` or inline as module docstring
- [ ] Key assumptions are explicit constants, not buried in logic
- [ ] Sensitivity to key parameters is discussed in docstring or notebook

**Notebooks**
- [ ] Runs clean from top-to-bottom on a fresh kernel
- [ ] Uses only files present in the repo (or documents where to obtain external data)
- [ ] Markdown cells explain what is being done and why

**General**
- [ ] PR description explains *what changed* and *why*
- [ ] Linked to relevant issue if one exists
- [ ] No credentials, API keys, or personal data committed

---

## Data Contribution Standards

1. **Always cite the source** — inline comment or a `sources.md` in the data subfolder
2. **Prefer open data** — SEBI, BSE, NSE, RBI, MoEFCC, MOSPI are all public
3. **Use consistent schemas** — check existing CSVs/parquets before adding new files
4. **Synthetic data** — clearly name files with `_synthetic` or `_illustrative` suffix
5. **Large files (>10MB)** — discuss in an issue before committing; we may use Git LFS or external links

---

## Model & Code Standards

- Follow existing module patterns (see `src/scenarios.py` for reference style)
- Use `dataclasses` or `TypedDict` for structured inputs
- Keep constants at module level, not hardcoded inside functions
- Functions should do one thing and be independently testable
- Use `pathlib.Path` for all file paths (no hardcoded strings)

---

## Reporting Issues

Use the issue templates in `.github/ISSUE_TEMPLATE/` for:
- 🐛 Bug reports
- 📊 Data gaps / update requests
- 🔬 Research gap suggestions
- 🔧 Model improvement proposals

---

## Code of Conduct

This project follows a simple standard: be respectful, be rigorous, cite your sources. Disagreements on methodology are welcome and encouraged — personal attacks are not.

---

*Questions? Open a discussion or tag a maintainer in an issue.*
