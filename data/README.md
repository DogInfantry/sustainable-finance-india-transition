# Data Inventory

This directory contains the research inputs and illustrative datasets used across the repository.

## Synthetic data notice

Some files in this repository are intentionally synthetic and exist to demonstrate schema, model inputs,
and documentation flow without redistributing proprietary market data. Synthetic files are either suffixed
with `_synthetic` or described as illustrative templates below.

## Top-level files

### `bank_source_ledger.csv`
Verified source ledger for public claims used in reporting modules.

### `example_corporate_profiles.csv`
Illustrative corporate profiles used for strategy and reporting examples.

### `india_transition_needs.csv`
Reference dataset describing subsector-level transition financing needs.

### `deal_economics.csv`
Illustrative commercial-layer deal archetypes with synthetic deal counts, ticket sizes, and fee pools.
Intended real-world sources: bank league tables, project finance deal databases, and internal pipeline analytics.

### `sector_capital_needs.csv`
Illustrative sector-level capital needs table aligned to transition-finance use cases in India.
Intended real-world sources: NITI Aayog, IEA India Energy Outlook, sector reports, and company capex plans.

### `bank_capabilities_template.csv`
Illustrative template showing how a bank capability profile can be structured for strategy analysis.
Intended real-world sources: annual reports, sustainability reports, and product framework pages.

## Subfolders

### `green_bonds/`
- `issuance_history_synthetic.csv`
- `pricing_spreads_synthetic.csv`

Intended real-world sources: SEBI, BSE, NSE, Climate Bonds Initiative, and market data terminals.

### `esg_scores/`
- `nifty50_esg_metrics_synthetic.csv`
- `sector_benchmarks_synthetic.csv`

Intended real-world sources: BRSR filings, MSCI ESG Research, Sustainalytics, Bloomberg ESG.

### `climate_scenarios/`
- `india_net_zero_2070.json`
- `sector_emissions_synthetic.csv`

Intended real-world sources: NITI Aayog, IEA, MoEFCC, IPCC, and sector disclosures.
