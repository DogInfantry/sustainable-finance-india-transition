# Sustainable Finance / India Energy Transition Work Sample

This repository is a consulting-style work sample on how sustainable finance can be deployed across India's energy transition, with product mapping and bank-specific positioning for **Standard Chartered**, **Deutsche Bank**, and **UBS**.

It is designed to feel like an associate-level strategy pack that sits between market research and a product-origination toolkit:

- a **country roadmap** for India's clean-energy and transition financing needs
- a **rule-based product mapping engine** that matches use cases to financing structures
- **bank-specific views** that translate public positioning into actionable India opportunities

## What Is In Scope

The repo focuses on the products most relevant to India's transition financing stack:

- green bonds
- green loans and green project finance
- sustainability-linked loans and bonds
- transition finance loans and bonds
- ESG-linked working capital / sustainable trade finance
- blended finance
- carbon-finance / results-based structures
- green securitisation for portfolio refinancing

## Source Discipline

The research layer is intentionally conservative.

- **Verified facts** are drawn only from official public materials from the banks: annual reports, sustainability reports, framework pages, press releases, public product pages, and bank India pages where available.
- **Illustrative numbers** are used only for the scenario model. They are clearly labeled as scenario assumptions and should not be read as market forecasts.
- If a bank-specific point could not be verified from the reviewed public sources, it is marked **not verified** instead of being filled in from memory.

Primary source references are stored in [data/bank_source_ledger.csv](/C:/Users/Anklesh/Documents/Codex/4-5-26/data/bank_source_ledger.csv).

## Project Components

### 1. Country Roadmap

[reports/india_transition_financing_roadmap.md](/C:/Users/Anklesh/Documents/Codex/4-5-26/reports/india_transition_financing_roadmap.md) frames India's transition financing stack across renewables, grids, storage, buildings, EV ecosystems and industrial decarbonisation. It also explains where project finance is better than bonds, and where SLLs fit better than green loans.

### 2. Product Mapping Engine

[reports/product_mapping_playbook.md](/C:/Users/Anklesh/Documents/Codex/4-5-26/reports/product_mapping_playbook.md) and [reports/product_mapping_table.csv](/C:/Users/Anklesh/Documents/Codex/4-5-26/reports/product_mapping_table.csv) translate subsectors and fictional borrower profiles into ranked financing recommendations. The engine is rule-based and explainable, not black-box ML.

### 3. Bank Views

[reports/bank_views_SC_DB_UBS.md](/C:/Users/Anklesh/Documents/Codex/4-5-26/reports/bank_views_SC_DB_UBS.md) compares how Standard Chartered, Deutsche Bank and UBS are publicly positioned in sustainable and transition finance, then turns that into India-specific commercial plays.

## Data and Methodology

### Data Files

- [data/india_transition_needs.csv](/C:/Users/Anklesh/Documents/Codex/4-5-26/data/india_transition_needs.csv)
  Transition subsectors, project characteristics and financing-relevant traits.
- [data/product_taxonomy.csv](/C:/Users/Anklesh/Documents/Codex/4-5-26/data/product_taxonomy.csv)
  Sustainable finance product definitions, borrower fit, covenant logic, advantages and constraints.
- [data/example_corporate_profiles.csv](/C:/Users/Anklesh/Documents/Codex/4-5-26/data/example_corporate_profiles.csv)
  Fictional but realistic India borrower cases across developers, utilities, corporates, EPCs, infra funds and financial institutions.
- [data/bank_source_ledger.csv](/C:/Users/Anklesh/Documents/Codex/4-5-26/data/bank_source_ledger.csv)
  Official source ledger used by the markdown reports.

### Scenario Method

- The roadmap uses a **directional** annual financing anchor based on public bank commentary that India's transition capital need is very large and can reach roughly the hundreds-of-billions-of-USD range over time.
- Subsector allocations are **illustrative scenario splits** used to test product fit.
- Funding-mix archetypes are stylized and should be treated as analytical scaffolding, not forecasts.

### Mapping Method

The product recommender scores each product against a use case using:

- capex intensity
- ticket size
- risk-sharing fit
- KPI readiness
- use-of-proceeds clarity
- transition stage
- borrower type
- bond-market readiness
- special-case biases for subsectors such as utility-scale renewables, industrial decarbonisation and EV ecosystems

## Repository Structure

```text
.
|-- README.md
|-- requirements.txt
|-- data
|   |-- bank_source_ledger.csv
|   |-- example_corporate_profiles.csv
|   |-- india_transition_needs.csv
|   `-- product_taxonomy.csv
|-- notebooks
|   |-- 01_india_transition_gap.ipynb
|   |-- 02_product_mapping_engine.ipynb
|   `-- 03_bank_views_SC_DB_UBS.ipynb
|-- reports
|   |-- bank_views_SC_DB_UBS.md
|   |-- india_transition_financing_roadmap.md
|   |-- product_mapping_playbook.md
|   `-- product_mapping_table.csv
`-- src
    |-- __init__.py
    |-- reporting.py
    |-- scenarios.py
    `-- taxonomy.py
```

## Setup

Use Python 3.11+.

```bash
pip install -r requirements.txt
```

## How To Re-Run

Open the notebooks directly, or execute them from the command line.

```bash
python -m jupyter nbconvert --to notebook --execute notebooks/01_india_transition_gap.ipynb --output-dir tmp
python -m jupyter nbconvert --to notebook --execute notebooks/02_product_mapping_engine.ipynb --output-dir tmp
python -m jupyter nbconvert --to notebook --execute notebooks/03_bank_views_SC_DB_UBS.ipynb --output-dir tmp
```

Each notebook regenerates the corresponding markdown report in `reports/`.

## Folder Structure Suggestion

If this analysis is reused in another repo or portfolio, keep the same separation:

- `data/` for the source-backed reference layer
- `src/` for reusable scenario, taxonomy and reporting logic
- `notebooks/` for transparent analytical workflows
- `reports/` for decision-maker-facing outputs

## Disclaimer

This project is an educational work sample, not investment advice, and is **not affiliated with Standard Chartered, Deutsche Bank, UBS, or any other institution**.
