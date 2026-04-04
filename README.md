# India Sustainable Finance Transition Roadmap

## Executive Summary

This repository is a portfolio-grade sustainable finance strategy sample focused on India's clean-energy and transition financing landscape.  
It combines a country financing roadmap, a rule-based product mapping engine, and bank-specific positioning for Standard Chartered, Deutsche Bank, and UBS.  
The product set mirrors real market practice across green, sustainability-linked, transition, blended, and capital-markets structures.  
Verified statements are anchored to official public bank materials, while scenario numbers are clearly marked as illustrative assumptions.  
All charts, reports, and appendix tables can be regenerated from source data with a single command: `python build.py`.

## What This Repo Does

The repository is designed to show how capital can be deployed across India's energy transition in a way that feels credible to sustainable-finance bankers and strategy teams.

- Builds an India transition financing roadmap across renewables, grids, storage, green buildings, EV ecosystems, industrial decarbonisation, and circular-economy use cases.
- Maps financing products to use cases using transparent, rule-based logic rather than black-box modeling.
- Compares how Standard Chartered, Deutsche Bank, and UBS are publicly positioned in sustainable and transition finance.
- Produces consulting-style markdown reports, figure outputs, and appendix tables suitable for a portfolio or interview discussion.

## Key Outputs

- [India transition roadmap](./reports/india_transition_financing_roadmap.md)
- [Product mapping playbook](./reports/product_mapping_playbook.md)
- [Bank views: Standard Chartered, Deutsche Bank, UBS](./reports/bank_views_SC_DB_UBS.md)
- [Strategy appendix](./reports/strategy_appendix.md)
- [Product mapping table (CSV)](./reports/product_mapping_table.csv)
- [Source ledger](./data/bank_source_ledger.csv)

## Repo Structure

```text
.
|-- .github/workflows/ci.yml
|-- build.py
|-- README.md
|-- requirements.txt
|-- data/
|   |-- bank_source_ledger.csv
|   |-- example_corporate_profiles.csv
|   |-- india_transition_needs.csv
|   `-- product_taxonomy.csv
|-- figures/
|   |-- bank_opportunity_matrix.png
|   |-- capital_channel_split.png
|   |-- product_recommendation_heatmap.png
|   `-- subsector_financing_allocation.png
|-- notebooks/
|   |-- 01_india_transition_gap.ipynb
|   |-- 02_product_mapping_engine.ipynb
|   `-- 03_bank_views_SC_DB_UBS.ipynb
|-- reports/
|   |-- assumption_register.csv
|   |-- bank_comparison_matrix.csv
|   |-- bank_views_SC_DB_UBS.md
|   |-- borrower_archetypes.csv
|   |-- india_sector_priority_matrix.csv
|   |-- india_transition_financing_roadmap.md
|   |-- product_mapping_playbook.md
|   |-- product_mapping_table.csv
|   |-- source_confidence_register.csv
|   `-- strategy_appendix.md
`-- src/
    |-- bank_views.py
    |-- figures.py
    |-- reporting.py
    |-- scenarios.py
    `-- taxonomy.py
```

## Methodology

### Research discipline

- Uses only official public materials from the banks for positioning claims: annual reports, sustainability reports, public framework pages, public product pages, press releases, and India pages where available.
- Stores those references in [data/bank_source_ledger.csv](./data/bank_source_ledger.csv).
- Treats any unverified point as `not verified` instead of filling gaps with unsupported claims.

### Scenario method

- Uses a directional annual financing anchor to size the India transition opportunity.
- Splits that anchor across subsectors using explicit, illustrative scenario weights.
- Allocates each subsector across broad capital channels: bank balance sheet, public markets, blended / DFI pools, and carbon-linked flows.

### Product mapping method

The product recommender scores financing structures against a use case using:

- capex intensity
- project or portfolio size
- risk-sharing fit
- KPI readiness
- use-of-proceeds clarity
- transition stage
- borrower type
- bond-market readiness
- subsector-specific commercial biases

### Instrument set

The taxonomy includes:

- green project finance and corporate green loans
- green bonds and green securitisation
- sustainability-linked loans, RCFs, and bonds
- transition finance loans and transition bond variants
- warehouse and aggregation facilities
- refinancing and take-out structures
- guarantees and partial risk-sharing facilities
- blended finance and carbon-linked structures
- advisory-led green / transition capital-markets solutions

## How To Run

Use Python 3.11+.

```bash
pip install -r requirements.txt
python build.py
```

That single build command regenerates:

- all markdown reports in `reports/`
- all portfolio figures in `figures/`
- all appendix CSV tables in `reports/`

## How To Regenerate Or Explore

- Source data lives in [data/](./data/).
- Reusable logic lives in [src/](./src/).
- Exploratory notebooks remain in [notebooks/](./notebooks/) for transparency, but `build.py` is the reproducible source-of-truth path for output generation.
- CI is configured in [`.github/workflows/ci.yml`](./.github/workflows/ci.yml) to run tests and rebuild outputs on push and pull request.

## Sample Outputs

### Financing allocation

![Subsector financing allocation](./figures/subsector_financing_allocation.png)

### Capital-channel split

![Capital-channel split](./figures/capital_channel_split.png)

### Product recommendation heatmap

![Product recommendation heatmap](./figures/product_recommendation_heatmap.png)

### Bank opportunity matrix

![Bank opportunity matrix](./figures/bank_opportunity_matrix.png)

## Limitations And Assumptions

- The scenario numbers are **illustrative**, not forecasts or market-size claims.
- Borrower archetypes are fictional and are included only to demonstrate product-fit logic.
- Product scoring is rule-based by design; it prioritises explainability over statistical optimization.
- Bank strategy recommendations combine verified public positioning with clearly labeled analyst inference.
- The work sample is educational and analytical only. It is not investment advice and is not affiliated with Standard Chartered, Deutsche Bank, UBS, or any other institution.
