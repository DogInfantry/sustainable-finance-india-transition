# Design Spec: India Sustainable Finance — Commercial Decision-Making Layer

**Date:** 2026-04-05
**Status:** Approved
**Audience:** Internal bank strategy teams
**Repo:** India Sustainable Finance Transition Roadmap

---

## 1. Context

The existing repository is a research-grade sustainable finance tool covering India's energy transition. It produces:
- Scenario-based financing gap analysis
- Rule-based product mapping across use cases
- Comparative bank positioning (SC, DB, UBS)
- Consulting-style markdown reports and PNG visualisations

This spec describes the **Commercial Decision-Making Layer** — a set of additive modules that upgrade the tool into a practical prioritisation and strategy engine for any bank's sustainable finance team.

**Hard constraint:** No existing outputs, data files, or source modules are modified or deleted.

---

## 2. Architectural Approach

**Approach B — New focused modules alongside existing ones.**

All new code lives in new files. Existing files are read-only from the perspective of this work. `build.py` is extended with a `build_commercial_layer()` function that runs **after** all existing build steps.

```
data/
  deal_economics.csv                  ← NEW
  bank_capabilities_template.csv      ← NEW

config/
  priority_weights.yaml               ← NEW

src/
  deal_economics.py                   ← NEW
  sector_priority.py                  ← NEW
  lifecycle.py                        ← NEW
  bank_strategy.py                    ← NEW
  commercial_report.py                ← NEW
  figures.py                          ← EXTENDED (new functions appended; existing untouched)

reports/
  deal_economics_summary.csv          ← NEW output
  sector_priority_ranking.csv         ← NEW output
  lifecycle_financing_matrix.csv      ← NEW output
  bank_strategy_output.csv            ← NEW output (3 sections)
  india_where_the_money_is.md         ← NEW report

figures/
  capital_allocation_by_sector.png    ← NEW
  product_dominance_by_sector.png     ← NEW
  lifecycle_financing_flow.png        ← NEW
  bank_opportunity_heatmap.png        ← NEW
```

All existing figures and reports remain untouched.

---

## 3. Module Designs

### 3.1 Deal Economics Layer

**Data file: `data/deal_economics.csv`**

One row per representative deal archetype. Covers all existing subsectors: Solar Utility-Scale, Wind Onshore, Wind Offshore, Battery Storage, EV Charging Infrastructure, Green Buildings, Industrial Decarbonisation, Circular Economy, Transmission & Grid.

Columns:
| Column | Type | Description |
|---|---|---|
| `subsector` | string | Subsector name |
| `deal_archetype` | string | e.g. Project Finance — Senior Secured |
| `deal_size_usd_mn` | float | Typical deal size (range midpoint) |
| `debt_pct` | float | % of deal financed by debt |
| `equity_pct` | float | % financed by equity |
| `grant_pct` | float | % from grants/concessional |
| `arranger_fee_bps` | float | Arranger/structuring fee in bps |
| `commitment_fee_bps` | float | Undrawn commitment fee in bps |
| `irr_expectation_pct` | float | Sponsor equity IRR expectation |
| `deal_count_annual_estimate` | int | Estimated annual deal count in India |
| `notes` | string | Source / assumption flag |

**Module: `src/deal_economics.py`**

Functions:
- `load_deal_economics(path) -> pd.DataFrame` — loads and validates the CSV
- `compute_annual_financing_volume(df) -> pd.DataFrame` — `deal_size × deal_count_annual_estimate` aggregated by subsector
- `compute_fee_pool(df) -> pd.DataFrame` — volume × weighted average fee (arranger + commitment), ranked by fee pool size
- `build_deal_economics_summary(output_path)` — orchestrates both computations, writes `reports/deal_economics_summary.csv`

All figures in the data file are marked as illustrative estimates; `notes` column carries the assumption flag.

---

### 3.2 Sector Prioritisation Model

**Config file: `config/priority_weights.yaml`**

```yaml
# Scoring weights for sector prioritisation.
# Values must sum to 1.0. Edit to reflect your institution's priorities.
weights:
  total_capital_required: 0.30   # Scale of deployment opportunity
  deal_frequency:         0.25   # Pipeline volume / deal activity
  bankability:            0.25   # Creditworthiness, collateral, offtake clarity
  fee_generation:         0.20   # Arranger + ongoing fee pool potential
```

**Module: `src/sector_priority.py`**

Functions:
- `load_weights(config_path) -> dict` — loads YAML; validates weights sum to 1.0; falls back to defaults if file missing
- `score_subsectors(transition_df, deal_economics_df, weights) -> pd.DataFrame` — scores each subsector 1–5 on each dimension using documented rule-based thresholds; applies weights to produce composite score
- `get_top_n(scored_df, n=5) -> pd.DataFrame` — returns top-N subsectors
- `build_sector_priority_ranking(output_path)` — orchestrates scoring, writes `reports/sector_priority_ranking.csv`

Scoring thresholds are defined as named constants at the top of the module, making assumptions explicit and auditable.

Output columns: `subsector`, `score_capital`, `score_frequency`, `score_bankability`, `score_fee`, `weighted_score`, `rank`, `top5_flag`.

---

### 3.3 Lifecycle Financing Model

**Module: `src/lifecycle.py`**

Stages: `Development`, `Construction`, `Operation`, `Refinancing`

For each `subsector × stage` cell:
- `primary_product` — dominant financing instrument
- `secondary_product` — complement or alternative
- `rationale` — one-line explanation

Data is defined as a structured dictionary within the module (not loaded from CSV) — fully transparent, no black-box logic.

Functions:
- `build_lifecycle_matrix() -> pd.DataFrame` — returns full subsector × stage × product table
- `export_lifecycle_matrix(output_path)` — writes `reports/lifecycle_financing_matrix.csv`
- `plot_lifecycle_heatmap(matrix_df, output_path)` — generates `figures/lifecycle_financing_flow.png`
  - Y-axis: subsectors
  - X-axis: lifecycle stages
  - Cell colour: primary product category (Loan = blue, Bond = green, Blended Finance = orange, Equity/Mezzanine = purple)
  - Single legend, consulting-grade styling consistent with existing figures

---

### 3.4 Bank Strategy Engine

**Data file: `data/bank_capabilities_template.csv`**

Generic profile. Any bank fills this in for their institution.

Columns:
| Column | Description |
|---|---|
| `capability` | Product/service name (e.g. Project Finance, Green Bond Structuring, SLL) |
| `strength` | 1–5 self-assessed score |
| `client_segment` | Corporate / Infrastructure / NBFC / DFI |
| `india_presence` | Yes / No / Limited |
| `notes` | Free text context |

Shipped with a representative "generic mid-tier bank" profile as a worked example.

**Module: `src/bank_strategy.py`**

Functions:
- `load_bank_profile(path) -> pd.DataFrame` — loads capabilities CSV
- `map_capabilities_to_sectors(capabilities_df, priority_df, lifecycle_df) -> pd.DataFrame` — for each top-5 sector, scores the bank's capability fit against dominant products at each lifecycle stage
- `get_top_strategic_plays(mapped_df) -> pd.DataFrame` — ranked table: sector + stage + recommended action
- `get_product_mix_recommendation(mapped_df) -> pd.DataFrame` — % allocation across product types
- `get_client_targeting_strategy(mapped_df, capabilities_df) -> pd.DataFrame` — segment + subsector + entry point
- `build_bank_strategy_output(bank_profile_path, output_path)` — orchestrates all three, writes `reports/bank_strategy_output.csv`

The engine is fully generic — no bank names hardcoded. Default profile path is the template file; can be overridden via CLI arg or config.

---

### 3.5 New Visualisations

All new figure functions added to `src/figures.py` as clearly separated new functions below the existing ones. Existing functions not modified.

| Function | Output | Description |
|---|---|---|
| `plot_capital_allocation_by_sector()` | `capital_allocation_by_sector.png` | Horizontal stacked bar: annual financing volume by subsector, stacked by capital channel |
| `plot_product_dominance_by_sector()` | `product_dominance_by_sector.png` | Heatmap: subsectors × product types, intensity = deal volume |
| `plot_lifecycle_heatmap()` | `lifecycle_financing_flow.png` | Heatmap: subsectors × lifecycle stages, colour = product category |
| `plot_bank_opportunity_heatmap()` | `bank_opportunity_heatmap.png` | Generic bank capability score × top-5 sectors × stages |

Visual styling consistent with existing figures: same font, colour palette, DPI, figure size conventions.

---

### 3.6 Report: "India Sustainable Finance: Where the Money Is"

**File:** `reports/india_where_the_money_is.md`

**Module:** `src/commercial_report.py`

Generated programmatically from module outputs. Tone: precise, direct, consulting-grade — modelled on McKinsey/Citi sector briefs. No filler language.

**Structure:**

1. **Executive Summary** — 3 key findings, market size anchor (total annual financing volume from deal economics), top-3 sectors by fee pool
2. **Sector Rankings** — full ranked table with composite scores and one-line rationale per sector; top-5 highlighted
3. **Deal Archetypes** — one archetype per top-5 sector: deal size, financing mix, fees, IRR expectation, typical borrower type
4. **Capital Stack Examples** — illustrative debt/equity/grant splits per archetype with notes on typical DFI involvement
5. **Lifecycle Financing Map** — embedded table from `lifecycle_financing_matrix.csv`; product evolution narrative for top-3 sectors
6. **Bank Strategy Recommendations** — generic strategic plays table, product mix recommendation, client targeting strategy; framed for internal strategy use
7. **Appendix** — assumption register (scoring thresholds, weight defaults, deal count methodology), data sources, methodology notes

All four new figures referenced inline.

---

## 4. Build Integration

`build.py` extended with:

```python
def build_commercial_layer():
    """Commercial decision-making layer — runs after core research outputs."""
    build_deal_economics_summary(...)
    build_sector_priority_ranking(...)
    build_lifecycle_matrix(...)
    build_bank_strategy_output(...)
    plot_capital_allocation_by_sector(...)
    plot_product_dominance_by_sector(...)
    plot_lifecycle_heatmap(...)
    plot_bank_opportunity_heatmap(...)
    build_commercial_report(...)
```

Called at the end of `main()`, after all existing build steps. If the commercial layer fails, existing outputs are unaffected.

---

## 5. Testing

New test file: `tests/test_commercial_layer.py`

Covers:
- `test_deal_economics_computes_fee_pool` — fee pool calculation correctness
- `test_sector_priority_weights_sum_to_one` — config validation
- `test_sector_priority_top5_returns_five` — ranking output shape
- `test_lifecycle_matrix_covers_all_subsectors` — completeness check
- `test_bank_strategy_output_has_three_sections` — output structure
- `test_commercial_report_generates_file` — smoke test

---

## 6. Key Constraints

- No existing file is modified except `build.py` (which is extended) and `src/figures.py` (new functions appended)
- All scenario numbers marked as illustrative; no investment advice claims
- All scoring thresholds documented as named constants
- Config file ships with sensible defaults; missing config falls back gracefully
- Bank strategy engine is fully generic — no institution names hardcoded
- Tone of generated report: internal strategy team audience, McKinsey/Citi brief style
