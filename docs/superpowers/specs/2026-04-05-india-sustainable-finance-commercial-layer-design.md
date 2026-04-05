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
  sector_capital_needs.csv            ← NEW (9 canonical subsectors + financing_need_usd_bn; does NOT replace india_transition_needs.csv)
  bank_capabilities_template.csv      ← NEW

config/                               ← NEW directory (create if absent)
  priority_weights.yaml               ← NEW

requirements.txt                      ← MODIFIED: add pyyaml>=6.0 (needed by load_weights())

src/
  constants.py                        ← NEW (canonical strings, path constants, mappings)
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
  bank_strategy_plays.csv             ← NEW output
  bank_strategy_product_mix.csv       ← NEW output
  bank_strategy_targeting.csv         ← NEW output
  india_where_the_money_is.md         ← NEW report

figures/
  capital_allocation_by_sector.png    ← NEW
  product_dominance_by_sector.png     ← NEW
  lifecycle_financing_flow.png        ← NEW
  bank_opportunity_heatmap.png        ← NEW
```

All existing figures and reports remain untouched.

---

## 3. `src/constants.py` — Single Source of Truth

All shared string identifiers and path constants live here. Every other module imports from this file — no raw strings duplicated across modules.

```python
import pandas as pd  # required for validate_subsectors() type annotation

# ── Canonical subsector names ─────────────────────────────────────────────
SUBSECTORS = [
    "Solar Utility-Scale",
    "Wind Onshore",
    "Wind Offshore",
    "Battery Storage",
    "EV Charging Infrastructure",
    "Green Buildings",
    "Industrial Decarbonisation",
    "Circular Economy",
    "Transmission & Grid",
]

# ── Lifecycle stages (fixed order) ────────────────────────────────────────
LIFECYCLE_STAGES = ["Development", "Construction", "Operation", "Refinancing"]

# ── Product categories for heatmap colouring ──────────────────────────────
PRODUCT_CATEGORIES = ["Loan", "Bond", "Blended Finance", "Equity/Mezzanine"]

# ── Default fallback for client segment ───────────────────────────────────
# Used by get_client_targeting_strategy() when no capability match is found.
DEFAULT_CLIENT_SEGMENT = "Infrastructure"

# ── Capital channel display names and CSV column mapping ──────────────────
# Used by plot_capital_allocation_by_sector().
# deal_economics.csv carries four channel columns; chart stacks them in this order.
CAPITAL_CHANNELS = ["Bank Debt", "Bonds", "Blended/DFI", "Equity"]
CAPITAL_CHANNEL_COLS = {
    "Bank Debt":   "bank_debt_pct",   # = debt_pct - bond_pct
    "Bonds":       "bond_pct",
    "Blended/DFI": "grant_pct",
    "Equity":      "equity_pct",
}

# ── Stage weights for product dominance volume attribution ─────────────────
# Used by plot_product_dominance_by_sector().
# Each subsector's annual_volume is distributed across stages by these weights,
# then attributed to the primary_product's PRODUCT_CATEGORY at each stage.
STAGE_VOLUME_WEIGHTS = {
    "Development":  0.10,
    "Construction": 0.50,
    "Operation":    0.30,
    "Refinancing":  0.10,
}

# ── Mapping from granular product names → PRODUCT_CATEGORIES ──────────────
# Used by plot_product_dominance_by_sector() and plot_lifecycle_heatmap().
# Note: SLL (Sustainability-Linked Loan) is classified as "Loan" — it is a
# loan instrument despite its sustainability-linked label. The figure legend
# and generated report include a footnote clarifying this.
PRODUCT_CATEGORY_MAP = {
    "Development Loan":           "Loan",
    "Working Capital Facility":   "Loan",
    "Green Project Finance":      "Loan",
    "SLL Refinancing":            "Loan",
    "SLL":                        "Loan",   # Sustainability-Linked Loan — loan instrument
    "Term Loan":                  "Loan",
    "Revolving Credit Facility":  "Loan",
    "Green Bond":                 "Bond",
    "Green Bond Tap":             "Bond",
    "Sustainability Bond":        "Bond",
    "Transition Bond":            "Bond",
    "Equity Bridge":              "Equity/Mezzanine",
    "Mezzanine Loan":             "Equity/Mezzanine",
    "Sponsor Equity":             "Equity/Mezzanine",
    "Blended Finance":            "Blended Finance",
    "DFI Co-lending":             "Blended Finance",
    "Guarantee":                  "Blended Finance",
    "Partial Credit Guarantee":   "Blended Finance",
    "Concessional Tranche":       "Blended Finance",
}

# ── Path constants (relative to repo root) ────────────────────────────────
DATA_DIR    = "data"
REPORTS_DIR = "reports"
FIGURES_DIR = "figures"
CONFIG_DIR  = "config"

DEAL_ECONOMICS_CSV       = f"{DATA_DIR}/deal_economics.csv"
BANK_TEMPLATE_CSV        = f"{DATA_DIR}/bank_capabilities_template.csv"
SECTOR_CAPITAL_NEEDS_CSV = f"{DATA_DIR}/sector_capital_needs.csv"  # NEW file; india_transition_needs.csv untouched
PRIORITY_WEIGHTS_YAML    = f"{CONFIG_DIR}/priority_weights.yaml"
DEFAULT_BANK_PROFILE_CSV = BANK_TEMPLATE_CSV   # overridable at build time


# ── Cross-module validation helper ────────────────────────────────────────
def validate_subsectors(df: pd.DataFrame, col: str) -> None:
    """Raise ValueError if df[col] contains values not in SUBSECTORS.

    - NaN values are treated as invalid and included in the error report.
    - Raises ValueError with a message listing all unrecognised values.
    - Does nothing if all values are valid.

    Usage: call immediately after loading any CSV that has a subsector column.
    """
```

---

## 4. Module Designs

### 4.1 Deal Economics Layer

**Data file: `data/deal_economics.csv`**

**Exactly one row per subsector** — one representative archetype per subsector. `load_deal_economics()` validates this (raises if any subsector appears more than once). `subsector` values must match `SUBSECTORS` exactly.

Columns:
| Column | Type | Description |
|---|---|---|
| `subsector` | string | Must match `constants.SUBSECTORS`; unique per row |
| `deal_archetype` | string | e.g. Project Finance — Senior Secured |
| `deal_size_usd_mn` | float | Typical deal size (range midpoint) |
| `debt_pct` | float | Total debt % (bank debt + bond), 0–100 |
| `bond_pct` | float | Bond financing sub-component of debt_pct, 0–100. bank_debt_pct = debt_pct − bond_pct |
| `equity_pct` | float | % financed by sponsor equity (0–100) |
| `grant_pct` | float | % from grants/concessional/DFI (0–100) |
| `arranger_fee_bps` | float | Arranger/structuring fee in basis points |
| `commitment_fee_bps` | float | Undrawn commitment fee in basis points |
| `irr_expectation_pct` | float | Sponsor equity IRR expectation (%) |
| `deal_count_annual_estimate` | int | Estimated annual deal count in India |
| `notes` | string | Source / assumption flag |

Constraint: `debt_pct + equity_pct + grant_pct` must equal 100 per row (validated on load, raises if violated). All values are illustrative estimates; `notes` carries the assumption flag.

**Module: `src/deal_economics.py`**

```python
def load_deal_economics(path: str = DEAL_ECONOMICS_CSV) -> pd.DataFrame:
    """Load and validate deal_economics.csv.
    Validations (all raise ValueError on failure):
    - validate_subsectors(df, 'subsector') — no unknown or NaN subsector values
    - Exactly one row per subsector (duplicates not permitted)
    - debt_pct + equity_pct + grant_pct == 100 per row (tolerance ±0.1)
    - bond_pct <= debt_pct per row"""

def compute_annual_financing_volume(df: pd.DataFrame) -> pd.DataFrame:
    """Input: raw deal_economics DataFrame.
    Returns DataFrame[subsector, annual_volume_usd_mn].
    annual_volume = deal_size_usd_mn × deal_count_annual_estimate, summed by subsector."""

def compute_fee_pool(df: pd.DataFrame) -> pd.DataFrame:
    """Input: raw deal_economics DataFrame.
    Returns DataFrame[subsector, annual_volume_usd_mn, weighted_fee_bps, fee_pool_usd_mn].
    weighted_fee_bps = (arranger_fee_bps + commitment_fee_bps) / 2.
    fee_pool_usd_mn = annual_volume_usd_mn × weighted_fee_bps / 10_000.
    Sorted descending by fee_pool_usd_mn."""

def build_deal_economics_summary(
    output_path: str = f"{REPORTS_DIR}/deal_economics_summary.csv",
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Orchestrate: load → compute_volume → compute_fee_pool → write CSV.
    Returns (raw_df, summary_df) where:
      raw_df     = full deal_economics DataFrame (all original columns)
      summary_df = merged volume + fee pool by subsector
    Both are returned so callers can use raw_df for deal archetypes and
    summary_df for aggregated stats without re-reading disk."""
```

---

### 4.2 Sector Prioritisation Model

**New data file: `data/sector_capital_needs.csv`**

The existing `data/india_transition_needs.csv` uses different subsector names (e.g. "Utility-scale renewables") and has no `financing_need_usd_bn` column. This new file provides the canonical capital need estimates aligned to `constants.SUBSECTORS`. It does **not** replace the existing file.

Required schema (one row per `SUBSECTORS` entry):

| Column | Type | Description |
|---|---|---|
| `subsector` | string | Must match `constants.SUBSECTORS` exactly |
| `financing_need_usd_bn` | float | Illustrative total capital required estimate (USD bn, annual) |
| `notes` | string | Assumption flag |

Representative values (illustrative, labelled as such):

| subsector | financing_need_usd_bn |
|---|---|
| Solar Utility-Scale | 18.0 |
| Wind Onshore | 10.0 |
| Wind Offshore | 3.0 |
| Battery Storage | 6.0 |
| EV Charging Infrastructure | 4.0 |
| Green Buildings | 5.0 |
| Industrial Decarbonisation | 8.0 |
| Circular Economy | 2.0 |
| Transmission & Grid | 12.0 |

---

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

**Scoring thresholds (named constants at top of `sector_priority.py`):**

`total_capital_required` — from `india_transition_needs.csv` column `financing_need_usd_bn`:
```python
CAPITAL_THRESHOLDS = [(50, 5), (20, 4), (10, 3), (5, 2), (0, 1)]
# (min_value_inclusive, score) — first matching threshold wins
```

`deal_frequency` — from `deal_economics.csv` column `deal_count_annual_estimate`:
```python
FREQUENCY_THRESHOLDS = [(20, 5), (10, 4), (5, 3), (2, 2), (0, 1)]
```

`bankability` — expert-judgment lookup; no external data source:
```python
BANKABILITY_SCORES = {
    "Solar Utility-Scale":        5,  # Mature PPAs, established lender base
    "Wind Onshore":               4,  # Good offtake, manageable site risk
    "Wind Offshore":              2,  # Nascent in India, high complexity
    "Battery Storage":            3,  # Growing; bankability improving
    "EV Charging Infrastructure": 2,  # Early stage, revenue uncertainty
    "Green Buildings":            3,  # Moderate; developer quality varies
    "Industrial Decarbonisation": 3,  # Corporate credit-backed
    "Circular Economy":           2,  # Thin track record in India
    "Transmission & Grid":        4,  # Regulated returns, government-backed
}
```

`fee_generation` — from `compute_fee_pool()` column `fee_pool_usd_mn`:
```python
FEE_THRESHOLDS = [(50, 5), (20, 4), (10, 3), (5, 2), (0, 1)]
```

**Module: `src/sector_priority.py`**

```python
def load_sector_capital_needs(path: str = SECTOR_CAPITAL_NEEDS_CSV) -> pd.DataFrame:
    """Load sector_capital_needs.csv (NEW file; does NOT use india_transition_needs.csv).
    Named differently from scenarios.load_transition_needs() to prevent silent misuse —
    the two functions have different contracts and different source files.
    Required schema (raises ValueError if columns are missing or subsectors unknown):
      - subsector: string — must match constants.SUBSECTORS exactly
      - financing_need_usd_bn: float — total capital required estimate
    Calls validate_subsectors(df, 'subsector')."""

def load_weights(config_path: str = PRIORITY_WEIGHTS_YAML) -> dict:
    """Load YAML weights using PyYAML (pyyaml>=6.0 required in requirements.txt).
    Uses Path(config_path).exists() — not a bare open() — so a missing config/ directory
    is handled identically to a missing file (both return False and trigger the warning path).
    If path does not exist: issues warnings.warn(f'Config {config_path} not found; using default weights.')
    and returns {total_capital_required:0.30, deal_frequency:0.25, bankability:0.25, fee_generation:0.20}.
    If path exists: loads YAML, validates abs(sum(values) - 1.0) <= 0.001 (raises ValueError if not)."""

def score_subsectors(
    sector_needs_df: pd.DataFrame, # from load_sector_capital_needs(); cols: subsector, financing_need_usd_bn
    raw_deal_df: pd.DataFrame,     # from load_deal_economics(); cols include subsector, deal_count_annual_estimate
    summary_deal_df: pd.DataFrame, # from build_deal_economics_summary()[1]; cols include subsector, fee_pool_usd_mn
    weights: dict,
) -> pd.DataFrame:
    """Score each subsector 1–5 on all four dimensions; apply weights.
    - total_capital_required: derived from sector_needs_df.financing_need_usd_bn  (parameter renamed from transition_df)
    - deal_frequency:         derived from raw_deal_df.deal_count_annual_estimate directly (one row per subsector; no aggregation needed)
    - bankability:            from BANKABILITY_SCORES lookup
    - fee_generation:         derived from summary_deal_df.fee_pool_usd_mn
    Returns DataFrame[subsector, score_capital, score_frequency,
    score_bankability, score_fee, weighted_score, rank, top5_flag].
    top5_flag = True for the top 5 rows by weighted_score (ties broken by score_capital)."""

def get_top_n(scored_df: pd.DataFrame, n: int = 5) -> pd.DataFrame:
    """Return top-N rows by weighted_score, ties broken by score_capital.
    If scored_df has fewer than n rows, returns all rows without error."""

def build_sector_priority_ranking(
    output_path: str = f"{REPORTS_DIR}/sector_priority_ranking.csv",
) -> pd.DataFrame:
    """Internal orchestration (all steps explicit):
      1. transition_df        = load_sector_capital_needs()
      2. raw_deal_df          = load_deal_economics()
      3. _, summary_deal_df   = build_deal_economics_summary()  # derives fee_pool_usd_mn via compute_fee_pool()
      4. weights              = load_weights()
      5. scored               = score_subsectors(transition_df, raw_deal_df, summary_deal_df, weights)
      6. Write scored to output_path as CSV
      7. Return scored (all 9 subsectors, with top5_flag column)
    Self-contained for independent testability. Duplicate disk reads vs
    build_commercial_layer() are acceptable — each function owns its own data loading."""
```

---

### 4.3 Lifecycle Financing Model

**Module: `src/lifecycle.py`**

Stages: `Development`, `Construction`, `Operation`, `Refinancing` (must match `constants.LIFECYCLE_STAGES`).

`LIFECYCLE_DATA` — full dictionary covering all 9 subsectors. All product name strings must exist as keys in `constants.PRODUCT_CATEGORY_MAP`.

```python
LIFECYCLE_DATA = {
    "Solar Utility-Scale": {
        "Development":  {"primary": "Development Loan",      "secondary": "Equity Bridge",        "rationale": "Pre-PPA risk; short-tenor development facility"},
        "Construction": {"primary": "Green Project Finance", "secondary": "Blended Finance",      "rationale": "Senior secured; DFI co-lending common at scale"},
        "Operation":    {"primary": "Green Bond",            "secondary": "SLL Refinancing",      "rationale": "Stable cashflow enables bond market access"},
        "Refinancing":  {"primary": "SLL Refinancing",       "secondary": "Green Bond Tap",       "rationale": "Rate optimisation; ESG KPI linkage adds pricing benefit"},
    },
    "Wind Onshore": {
        "Development":  {"primary": "Development Loan",      "secondary": "Equity Bridge",        "rationale": "Site development and permitting phase"},
        "Construction": {"primary": "Green Project Finance", "secondary": "DFI Co-lending",       "rationale": "Senior secured; multilateral co-lending available"},
        "Operation":    {"primary": "Green Bond",            "secondary": "Term Loan",            "rationale": "Long-tenor stable cashflow; bond execution viable"},
        "Refinancing":  {"primary": "SLL Refinancing",       "secondary": "Green Bond Tap",       "rationale": "Optimise cost of capital with sustainability linkage"},
    },
    "Wind Offshore": {
        "Development":  {"primary": "Development Loan",      "secondary": "Mezzanine Loan",       "rationale": "High complexity; mezzanine often required for risk layering"},
        "Construction": {"primary": "Blended Finance",       "secondary": "Green Project Finance","rationale": "Nascent market; concessional capital essential to bridge viability gap"},
        "Operation":    {"primary": "Green Project Finance", "secondary": "Green Bond",           "rationale": "Track record builds over first operating years before bond market access"},
        "Refinancing":  {"primary": "Green Bond",            "secondary": "SLL Refinancing",      "rationale": "Refinancing onto bond market as asset class matures"},
    },
    "Battery Storage": {
        "Development":  {"primary": "Development Loan",      "secondary": "Equity Bridge",        "rationale": "Technology and offtake risk managed at development stage"},
        "Construction": {"primary": "Green Project Finance", "secondary": "Partial Credit Guarantee", "rationale": "PCG from DFIs increasingly used to enhance bankability"},
        "Operation":    {"primary": "SLL",                   "secondary": "Green Bond",           "rationale": "SLL suitable given measurable storage/grid KPIs"},
        "Refinancing":  {"primary": "Green Bond",            "secondary": "SLL Refinancing",      "rationale": "Bond market access as storage asset class matures in India"},
    },
    "EV Charging Infrastructure": {
        "Development":  {"primary": "Working Capital Facility", "secondary": "Development Loan",  "rationale": "Fragmented, asset-light; working capital more relevant than project finance"},
        "Construction": {"primary": "Green Project Finance",    "secondary": "Blended Finance",   "rationale": "Anchor sites project-financed; DFI support for network buildout"},
        "Operation":    {"primary": "SLL",                      "secondary": "Revolving Credit Facility", "rationale": "SLL with utilisation/uptime KPIs; revolving facility for capex flexibility"},
        "Refinancing":  {"primary": "Sustainability Bond",      "secondary": "SLL Refinancing",   "rationale": "Portfolio aggregation enables bond market access at scale"},
    },
    "Green Buildings": {
        "Development":  {"primary": "Development Loan",      "secondary": "Equity Bridge",        "rationale": "Developer finance at pre-construction stage"},
        "Construction": {"primary": "Green Project Finance", "secondary": "Concessional Tranche", "rationale": "Green certification unlocks preferential pricing; some DFI support"},
        "Operation":    {"primary": "Sustainability Bond",   "secondary": "SLL",                  "rationale": "Portfolio of certified buildings suitable for sustainability bond"},
        "Refinancing":  {"primary": "SLL Refinancing",       "secondary": "Green Bond Tap",       "rationale": "Ongoing green certification metrics link to margin ratchets"},
    },
    "Industrial Decarbonisation": {
        "Development":  {"primary": "Working Capital Facility", "secondary": "Development Loan",  "rationale": "Technology assessment and feasibility; corporate credit-backed"},
        "Construction": {"primary": "SLL",                      "secondary": "Green Project Finance", "rationale": "SLL against decarbonisation KPIs; project finance for discrete capex"},
        "Operation":    {"primary": "Transition Bond",          "secondary": "SLL",               "rationale": "Transition bond framework appropriate for hard-to-abate sector"},
        "Refinancing":  {"primary": "Sustainability Bond",      "secondary": "SLL Refinancing",   "rationale": "Refinancing as decarbonisation pathway matures"},
    },
    "Circular Economy": {
        "Development":  {"primary": "Development Loan",      "secondary": "Concessional Tranche", "rationale": "Thin track record; concessional tranche often needed to attract senior debt"},
        "Construction": {"primary": "Blended Finance",       "secondary": "Green Project Finance","rationale": "DFI/blended finance essential given nascent commercial viability"},
        "Operation":    {"primary": "Green Bond",            "secondary": "SLL",                  "rationale": "Operating asset generates cashflow; green bond if use-of-proceeds clear"},
        "Refinancing":  {"primary": "SLL Refinancing",       "secondary": "Sustainability Bond",  "rationale": "SLL with circularity metrics for refinancing phase"},
    },
    "Transmission & Grid": {
        "Development":  {"primary": "Development Loan",      "secondary": "Guarantee",            "rationale": "Regulated utility; government guarantee reduces cost of development debt"},
        "Construction": {"primary": "Green Project Finance", "secondary": "DFI Co-lending",       "rationale": "Large-ticket senior secured; multilateral co-lending common"},
        "Operation":    {"primary": "Green Bond",            "secondary": "Sustainability Bond",  "rationale": "Regulated cashflow ideal for long-duration bond"},
        "Refinancing":  {"primary": "Green Bond Tap",        "secondary": "SLL Refinancing",      "rationale": "Tap existing green bond programme; SLL where grid KPIs measurable"},
    },
}
```

```python
def build_lifecycle_matrix() -> pd.DataFrame:
    """Returns DataFrame[subsector, stage, primary_product, secondary_product, rationale].
    Validates all SUBSECTORS present; validates all LIFECYCLE_STAGES present per subsector;
    validates all product strings exist in PRODUCT_CATEGORY_MAP."""

def export_lifecycle_matrix(
    output_path: str = f"{REPORTS_DIR}/lifecycle_financing_matrix.csv",
) -> pd.DataFrame:
    """Write matrix to CSV. Returns DataFrame."""
```

`plot_lifecycle_heatmap` lives exclusively in `src/figures.py`. `lifecycle.py` does not define it.

---

### 4.4 New Visualisations

All new figure functions appended to `src/figures.py`. Existing functions not modified. Styling: DejaVu Sans, 150 DPI, (12, 7) figure size, tight layout — matching existing conventions.

```python
def plot_capital_allocation_by_sector(
    volume_df: pd.DataFrame,       # from compute_annual_financing_volume(); cols: subsector, annual_volume_usd_mn
    raw_deal_df: pd.DataFrame,     # from load_deal_economics(); cols include debt_pct, bond_pct, equity_pct, grant_pct
    output_path: str = f"{FIGURES_DIR}/capital_allocation_by_sector.png",
) -> None:
    """Horizontal stacked bar: annual financing volume by subsector,
    stacked by four capital channels defined in constants.CAPITAL_CHANNELS.
    Channel split computation per subsector:
      bank_debt_vol = annual_volume × (debt_pct - bond_pct) / 100
      bond_vol      = annual_volume × bond_pct / 100
      blended_vol   = annual_volume × grant_pct / 100
      equity_vol    = annual_volume × equity_pct / 100
    Join: volume_df joined to raw_deal_df on 'subsector' (inner join; one row each).
    Stacking order: Bank Debt, Bonds, Blended/DFI, Equity (left to right)."""

def plot_product_dominance_by_sector(
    lifecycle_df: pd.DataFrame,    # from export_lifecycle_matrix(); cols: subsector, stage, primary_product
    raw_deal_df: pd.DataFrame,     # from load_deal_economics(); cols: subsector, deal_size_usd_mn, deal_count_annual_estimate
    output_path: str = f"{FIGURES_DIR}/product_dominance_by_sector.png",
) -> None:
    """Heatmap: subsectors (Y) × PRODUCT_CATEGORIES (X).
    Algorithm:
      1. Compute annual_volume per subsector from raw_deal_df (one row each; no aggregation needed).
      2. Join lifecycle_df to volume on 'subsector' (inner join).
      3. For each subsector × stage cell, compute stage_volume = annual_volume × STAGE_VOLUME_WEIGHTS[stage].
      4. Map primary_product → PRODUCT_CATEGORY via PRODUCT_CATEGORY_MAP.
      5. Sum stage_volume by subsector × PRODUCT_CATEGORY.
      6. Pivot to subsectors (Y) × PRODUCT_CATEGORIES (X) with sum of stage_volume as cell value.
    Cell intensity = sum of stage_volume_usd_mn. Zero-volume cells rendered as white.
    Legend footnote: 'SLL classified as Loan (bank lending instrument).'"""

def plot_lifecycle_heatmap(
    matrix_df: pd.DataFrame,       # from export_lifecycle_matrix()
    output_path: str = f"{FIGURES_DIR}/lifecycle_financing_flow.png",
) -> None:
    """Heatmap: subsectors (Y) × LIFECYCLE_STAGES (X).
    Cell colour = PRODUCT_CATEGORY of primary_product (via PRODUCT_CATEGORY_MAP):
      Loan = blue (#2166ac), Bond = green (#1a9641),
      Blended Finance = orange (#f46d43), Equity/Mezzanine = purple (#762a83).
    Cell text = primary_product name. Single legend."""

def plot_bank_opportunity_heatmap(
    mapped_df: pd.DataFrame,       # from map_capabilities_to_sectors(); cols: subsector, stage, fit_score_normalised
    output_path: str = f"{FIGURES_DIR}/bank_opportunity_heatmap.png",
) -> None:
    """Heatmap: sectors (Y) × LIFECYCLE_STAGES (X).
    Expects a pre-filtered DataFrame — caller is responsible for passing only the
    desired subsectors (e.g. top-5). Function renders all subsectors present in
    mapped_df without further filtering.
    Cell intensity = fit_score_normalised (0–5, sequential blue palette).
    Cell text = fit_score_normalised rounded to 1dp. No bank names."""
```

---

### 4.5 Bank Strategy Engine

**Data file: `data/bank_capabilities_template.csv`**

Shipped with a representative "generic mid-tier bank" worked example. `capability` values must match keys in `PRODUCT_CATEGORY_MAP`.

Columns:
| Column | Type | Description |
|---|---|---|
| `capability` | string | Product/service; must match keys in `PRODUCT_CATEGORY_MAP` |
| `strength` | int 1–5 | Self-assessed capability score |
| `client_segment` | string | Corporate / Infrastructure / NBFC / DFI |
| `india_presence` | string | Yes / No / Limited |
| `notes` | string | Free text |

**Module: `src/bank_strategy.py`**

`map_capabilities_to_sectors` algorithm:
- Lookup method: for each product string (primary or secondary), case-fold both sides and find all matching rows in `capabilities_df`. If multiple rows match (same product listed twice with different segments), take `max(strength)`. If no match, use 0.
- For each `top-N sector × stage`:
  - `primary_strength` = max matched strength for `primary_product`, or 0
  - `secondary_strength` = max matched strength for `secondary_product`, or 0
  - `fit_score` = `primary_strength + 0.5 × secondary_strength` (max 7.5)
  - `fit_score_normalised` = `round(fit_score / 7.5 * 5, 2)` (scale 0–5)
- Unmatched capabilities are not penalised

```python
def load_bank_profile(
    path: str = DEFAULT_BANK_PROFILE_CSV,
) -> pd.DataFrame:
    """Load capabilities CSV. Validates required columns exist."""

def map_capabilities_to_sectors(
    capabilities_df: pd.DataFrame,   # from load_bank_profile()
    priority_df: pd.DataFrame,       # pre-filtered top-N DataFrame (caller must filter before passing)
    lifecycle_df: pd.DataFrame,      # from export_lifecycle_matrix()
) -> pd.DataFrame:
    """Returns DataFrame[subsector, stage, primary_product, secondary_product,
    primary_strength, secondary_strength, fit_score, fit_score_normalised]."""

def get_top_strategic_plays(mapped_df: pd.DataFrame) -> pd.DataFrame:
    """Returns DataFrame[rank, subsector, stage, recommended_action, fit_score_normalised].
    recommended_action: 'Lead Arranger' if fit_score_normalised >= 4,
    'Co-Arranger' if >= 2.5, 'Build Capability / Partner' otherwise.
    Sorted descending by fit_score_normalised."""

def get_product_mix_recommendation(mapped_df: pd.DataFrame) -> pd.DataFrame:
    """Returns DataFrame[product_category, total_fit_score, recommended_allocation_pct].
    For each PRODUCT_CATEGORY, sum fit_score_normalised across all subsector×stage cells
    where primary_product maps to that category (via PRODUCT_CATEGORY_MAP).
    allocation_pct = total_fit_score / sum(all total_fit_scores) × 100.
    Zero-division guard: if sum of all scores == 0, return equal allocation (25% per category)."""

def get_client_targeting_strategy(
    mapped_df: pd.DataFrame,
    capabilities_df: pd.DataFrame,
) -> pd.DataFrame:
    """Returns DataFrame[subsector, client_segment, entry_stage, entry_point, rationale].
    entry_stage = stage with highest fit_score_normalised for each subsector.
    Tie-breaking: first occurrence in constants.LIFECYCLE_STAGES order (Development < Construction < Operation < Refinancing).
    entry_point = primary_product at that stage.
    client_segment = capabilities_df['client_segment'] for the matching capability (case-insensitive match on entry_point);
    if multiple matches, take the row with highest strength; falling back to constants.DEFAULT_CLIENT_SEGMENT if no match."""

def build_bank_strategy_output(
    bank_profile_path: str = DEFAULT_BANK_PROFILE_CSV,
    priority_df: pd.DataFrame | None = None,   # FULL ranked DataFrame (all 9 subsectors); if None, calls build_sector_priority_ranking() internally
    lifecycle_df: pd.DataFrame | None = None,  # from export_lifecycle_matrix(); if None, calls export_lifecycle_matrix() internally
    n_sectors: int = 5,                        # number of top sectors to map; default 5
    plays_path: str = f"{REPORTS_DIR}/bank_strategy_plays.csv",
    mix_path: str = f"{REPORTS_DIR}/bank_strategy_product_mix.csv",
    targeting_path: str = f"{REPORTS_DIR}/bank_strategy_targeting.csv",
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Orchestration (all steps explicit):
      1. capabilities = load_bank_profile(bank_profile_path)
      2. priority_df  = build_sector_priority_ranking() if priority_df is None
      3. lifecycle_df = export_lifecycle_matrix() if lifecycle_df is None
      4. top_n        = get_top_n(priority_df, n_sectors)   ← filtering happens HERE, not before
      5. Guard: if len(top_n) == 0, raise ValueError('No subsectors to map — check sector_priority output.')
      6. mapped       = map_capabilities_to_sectors(capabilities, top_n, lifecycle_df)
      7. plays        = get_top_strategic_plays(mapped)
      8. mix          = get_product_mix_recommendation(mapped)
      9. targeting    = get_client_targeting_strategy(mapped, capabilities)
      10. Write plays/mix/targeting to three CSVs
      11. Return (plays_df, mix_df, targeting_df)
    Caller in build_commercial_layer() passes the full priority_df and lifecycle_df;
    this function owns the get_top_n filtering step."""
```

---

### 4.6 Report: "India Sustainable Finance: Where the Money Is"

**File:** `reports/india_where_the_money_is.md`

**Module:** `src/commercial_report.py`

```python
def build_commercial_report(
    priority_df: pd.DataFrame,     # full scored DataFrame from build_sector_priority_ranking()
    raw_deal_df: pd.DataFrame,     # raw deal_economics DataFrame (for archetypes: size, fees, IRR)
    summary_deal_df: pd.DataFrame, # aggregated summary (for market size stats)
    lifecycle_df: pd.DataFrame,    # from export_lifecycle_matrix()
    plays_df: pd.DataFrame,        # from get_top_strategic_plays()
    mix_df: pd.DataFrame,          # from get_product_mix_recommendation()
    targeting_df: pd.DataFrame,    # from get_client_targeting_strategy()
    output_path: str = f"{REPORTS_DIR}/india_where_the_money_is.md",
) -> None:
    """Generate consulting-style strategy report from module outputs."""
```

Tone: precise, direct, no filler — modelled on McKinsey/Citi sector briefs. Internal strategy team audience.

**Report structure:**

1. **Executive Summary** — 3 key findings; total annual financing volume (from `summary_deal_df`); top-3 sectors by fee pool
2. **Sector Rankings** — full ranked table (all 9 subsectors); composite scores; one-line rationale per sector; top-5 flagged
3. **Deal Archetypes** — one archetype per top-5 sector drawn from `raw_deal_df`: deal size, financing mix, fees, IRR, typical borrower type
4. **Capital Stack Examples** — illustrative debt/equity/grant splits per archetype; notes on DFI involvement
5. **Lifecycle Financing Map** — embedded table from `lifecycle_df`; product evolution narrative for top-3 sectors
6. **Bank Strategy Recommendations** — strategic plays table, product mix table, client targeting table; all generic (no bank names)
7. **Appendix** — scoring thresholds (from `sector_priority.py` constants), weight defaults, deal count methodology, data sources

All four new figures referenced inline using paths relative to the report file's location (`reports/`): e.g. `../figures/capital_allocation_by_sector.png`. This ensures correct rendering when the markdown file is opened directly from the filesystem.

---

## 5. Build Integration

```python
# build.py — additions (all existing code unchanged)
import argparse
from src.constants import DEFAULT_BANK_PROFILE_CSV

def build_commercial_layer(bank_profile_path: str = DEFAULT_BANK_PROFILE_CSV) -> None:
    """Commercial decision-making layer — runs after core research outputs."""
    from src.deal_economics import (load_deal_economics, build_deal_economics_summary,
                                    compute_annual_financing_volume)
    from src.sector_priority import build_sector_priority_ranking, get_top_n
    from src.lifecycle import export_lifecycle_matrix
    from src.bank_strategy import (build_bank_strategy_output, load_bank_profile,
                                   map_capabilities_to_sectors)
    from src.figures import (plot_capital_allocation_by_sector, plot_product_dominance_by_sector,
                             plot_lifecycle_heatmap, plot_bank_opportunity_heatmap)
    from src.commercial_report import build_commercial_report

    # Load raw deal data once — reused by multiple downstream functions
    raw_deal_df, summary_deal_df = build_deal_economics_summary()

    vol_df    = compute_annual_financing_volume(raw_deal_df)
    priority  = build_sector_priority_ranking()   # full 9-subsector DataFrame
    lifecycle = export_lifecycle_matrix()

    # build_bank_strategy_output owns the get_top_n(5) filtering step internally
    plays, mix, targeting = build_bank_strategy_output(
        bank_profile_path=bank_profile_path,
        priority_df=priority,    # full ranked DataFrame — function filters to top-N
        lifecycle_df=lifecycle,
    )

    plot_capital_allocation_by_sector(vol_df, raw_deal_df)
    plot_product_dominance_by_sector(lifecycle, raw_deal_df)
    plot_lifecycle_heatmap(lifecycle)

    # For the opportunity heatmap, map capabilities against top-5 only
    top5 = get_top_n(priority, 5)
    capabilities = load_bank_profile(bank_profile_path)
    mapped = map_capabilities_to_sectors(capabilities, top5, lifecycle)
    plot_bank_opportunity_heatmap(mapped)  # expects pre-filtered DataFrame

    build_commercial_report(priority, raw_deal_df, summary_deal_df,
                            lifecycle, plays, mix, targeting)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--bank-profile",
        default=DEFAULT_BANK_PROFILE_CSV,
        help="Path to bank capabilities CSV (default: data/bank_capabilities_template.csv)",
    )
    args = parser.parse_args()

    # ... existing build steps unchanged — commercial layer runs last ...
    build_commercial_layer(bank_profile_path=args.bank_profile)
```

If `build_commercial_layer()` raises, existing outputs are unaffected (it runs last).

---

## 6. Testing

New test file: `tests/test_commercial_layer.py`

| Test | What it checks |
|---|---|
| `test_deal_economics_fee_pool_formula` | arranger_fee=100bps, commitment_fee=50bps, volume=200 USD mn → weighted_fee=75bps, fee_pool=1.5 USD mn |
| `test_deal_economics_returns_raw_and_summary` | `build_deal_economics_summary()` returns 2-tuple; raw_df has `bond_pct`; summary_df has `fee_pool_usd_mn` |
| `test_deal_economics_duplicate_subsector_raises` | `load_deal_economics()` raises ValueError if any subsector appears more than once |
| `test_deal_economics_channel_pcts_sum_to_100` | `load_deal_economics()` raises if debt+equity+grant ≠ 100 |
| `test_sector_priority_weights_valid_passes` | `load_weights()` returns dict without error when weights sum to 1.0 |
| `test_sector_priority_weights_invalid_raises` | `load_weights()` raises ValueError when weights sum ≠ 1.0 |
| `test_sector_priority_weights_missing_file_warns` | `load_weights()` issues `warnings.warn` and returns defaults when YAML not found |
| `test_sector_priority_top5_returns_five` | `get_top_n(df, 5)` returns exactly 5 rows |
| `test_sector_priority_fewer_than_n_ok` | `get_top_n(df, 5)` on 3-row df returns 3 rows without error |
| `test_lifecycle_matrix_covers_all_subsectors` | All 9 SUBSECTORS × 4 stages present; no missing cells |
| `test_lifecycle_matrix_products_in_category_map` | All primary/secondary product strings exist in PRODUCT_CATEGORY_MAP |
| `test_bank_strategy_three_csvs_written` | Three output CSVs exist and are non-empty after run |
| `test_bank_strategy_plays_columns` | Plays output has rank, subsector, stage, recommended_action, fit_score_normalised |
| `test_bank_strategy_empty_priority_raises` | `build_bank_strategy_output()` raises ValueError on empty priority_df |
| `test_bank_strategy_zero_fit_equal_allocation` | `get_product_mix_recommendation()` returns 25% per category when all fit scores are 0 |
| `test_bank_strategy_tiebeak_uses_lifecycle_order` | `get_client_targeting_strategy()` resolves tie by first occurrence in LIFECYCLE_STAGES |
| `test_commercial_report_generates_file` | Output file exists, is non-empty, and contains `../figures/` relative paths |
| `test_validate_subsectors_raises_on_unknown` | Raises ValueError on unrecognised name |
| `test_validate_subsectors_raises_on_nan` | Raises ValueError on NaN value |

---

## 7. Key Constraints

- No existing file modified except `build.py` (extended) and `src/figures.py` (new functions appended below existing ones)
- All scenario numbers marked as illustrative; no investment advice claims
- All scoring thresholds defined as named constants — auditable, not buried in logic
- Config file ships with sensible defaults; missing config falls back gracefully
- Bank strategy engine fully generic — no institution names hardcoded anywhere
- Subsector strings centralised in `src/constants.py`; `validate_subsectors()` enforces consistency at load time
- All product name strings must exist in `PRODUCT_CATEGORY_MAP` — validated at matrix build time
- `build_commercial_layer()` loads raw deal data once via `build_deal_economics_summary()` and threads it through figure functions; `build_sector_priority_ranking()` performs its own self-contained load for independent testability
- Tone of generated report: internal strategy team, McKinsey/Citi brief style
