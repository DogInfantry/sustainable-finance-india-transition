# India Sustainable Finance — Commercial Layer Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a commercial decision-making layer to the existing research repo — deal economics, sector prioritisation, lifecycle financing model, generic bank strategy engine, four new visualisations, and a consulting-style strategy report — without touching any existing file except `build.py` and `src/figures.py`.

**Architecture:** New focused modules in `src/` (constants, deal_economics, sector_priority, lifecycle, bank_strategy, commercial_report) each with a single responsibility, wired together by a new `build_commercial_layer()` appended to `build.py`. All shared strings (subsector names, product names) centralised in `src/constants.py`; validated at load time.

**Tech Stack:** Python 3.11+, pandas 2.2+, matplotlib 3.9+, pyyaml 6.0+, pytest 8.3+

**Spec:** `docs/superpowers/specs/2026-04-05-india-sustainable-finance-commercial-layer-design.md`

---

## File Map

| File | Action | Responsibility |
|---|---|---|
| `requirements.txt` | Modify | Add `pyyaml>=6.0` |
| `config/priority_weights.yaml` | Create | Tunable sector scoring weights |
| `data/deal_economics.csv` | Create | Representative deal archetypes (9 subsectors) |
| `data/sector_capital_needs.csv` | Create | Canonical capital need estimates per subsector |
| `data/bank_capabilities_template.csv` | Create | Generic bank capability profile template |
| `src/constants.py` | Create | Canonical strings, path constants, PRODUCT_CATEGORY_MAP |
| `src/deal_economics.py` | Create | Load/validate deals; compute volume & fee pool |
| `src/sector_priority.py` | Create | Score & rank subsectors; load weights |
| `src/lifecycle.py` | Create | Lifecycle stage × product matrix |
| `src/bank_strategy.py` | Create | Generic bank capability mapper |
| `src/commercial_report.py` | Create | Generate "Where the Money Is" markdown report |
| `src/figures.py` | Extend | Append 4 new figure functions (existing untouched) |
| `build.py` | Extend | Add `build_commercial_layer()` + argparse to `main()` |
| `tests/test_commercial_layer.py` | Create | All tests for new modules |

---

## Task 1: Scaffold — Data Files, Config, Requirements

**Files:**
- Create: `config/priority_weights.yaml`
- Create: `data/deal_economics.csv`
- Create: `data/sector_capital_needs.csv`
- Create: `data/bank_capabilities_template.csv`
- Modify: `requirements.txt`

- [ ] **Step 1: Add pyyaml to requirements.txt**

Open `requirements.txt` and append:
```
pyyaml>=6.0
```

- [ ] **Step 2: Create config directory and priority_weights.yaml**

```yaml
# config/priority_weights.yaml
# Scoring weights for sector prioritisation.
# Values must sum to 1.0. Edit to reflect your institution's priorities.
weights:
  total_capital_required: 0.30   # Scale of deployment opportunity
  deal_frequency:         0.25   # Pipeline volume / deal activity
  bankability:            0.25   # Creditworthiness, collateral, offtake clarity
  fee_generation:         0.20   # Arranger + ongoing fee pool potential
```

- [ ] **Step 3: Create data/sector_capital_needs.csv**

```csv
subsector,financing_need_usd_bn,notes
Solar Utility-Scale,18.0,Illustrative estimate — annual deployment target
Wind Onshore,10.0,Illustrative estimate — annual deployment target
Wind Offshore,3.0,Illustrative estimate — nascent market
Battery Storage,6.0,Illustrative estimate — annual deployment target
EV Charging Infrastructure,4.0,Illustrative estimate — annual deployment target
Green Buildings,5.0,Illustrative estimate — annual deployment target
Industrial Decarbonisation,8.0,Illustrative estimate — annual deployment target
Circular Economy,2.0,Illustrative estimate — early-stage market
Transmission & Grid,12.0,Illustrative estimate — annual deployment target
```

- [ ] **Step 4: Create data/deal_economics.csv**

One row per subsector. `debt_pct + equity_pct + grant_pct = 100`. `bond_pct <= debt_pct`.

```csv
subsector,deal_archetype,deal_size_usd_mn,debt_pct,bond_pct,equity_pct,grant_pct,arranger_fee_bps,commitment_fee_bps,irr_expectation_pct,deal_count_annual_estimate,notes
Solar Utility-Scale,Project Finance — Senior Secured,150.0,75.0,20.0,25.0,0.0,120,50,12.0,40,Illustrative — based on observed India solar PF transactions
Wind Onshore,Project Finance — Senior Secured,120.0,70.0,15.0,30.0,0.0,110,45,13.0,25,Illustrative — based on India wind PF market
Wind Offshore,Project Finance — Blended,300.0,60.0,10.0,25.0,15.0,175,65,15.0,3,Illustrative — nascent India offshore wind market
Battery Storage,Project Finance — PCG Enhanced,80.0,65.0,10.0,25.0,10.0,140,55,14.0,15,Illustrative — BESS project finance with DFI support
EV Charging Infrastructure,Corporate/Portfolio Finance,30.0,55.0,5.0,35.0,10.0,100,40,16.0,20,Illustrative — EV infrastructure portfolio deals
Green Buildings,Developer Finance,40.0,60.0,10.0,30.0,10.0,90,35,14.0,18,Illustrative — green certified commercial RE
Industrial Decarbonisation,SLL — Corporate,200.0,70.0,20.0,30.0,0.0,95,40,13.0,12,Illustrative — large corporate SLL for decarbonisation capex
Circular Economy,Blended Finance,25.0,50.0,5.0,30.0,20.0,130,50,15.0,8,Illustrative — circular economy blended transactions
Transmission & Grid,Project Finance — Regulated,400.0,80.0,25.0,20.0,0.0,100,40,11.0,10,Illustrative — regulated transmission asset finance
```

- [ ] **Step 5: Create data/bank_capabilities_template.csv**

```csv
capability,strength,client_segment,india_presence,notes
Green Project Finance,4,Infrastructure,Yes,Core product — project finance team
Development Loan,3,Infrastructure,Yes,Deal origination capability
Green Bond,3,Corporate,Yes,DCM capability for green bond structuring
SLL,4,Corporate,Yes,Sustainability-linked loan structuring
Blended Finance,2,Infrastructure,Limited,Partnership with DFIs; limited own balance sheet
DFI Co-lending,2,Infrastructure,Limited,Selective co-lending arrangements
SLL Refinancing,3,Corporate,Yes,Refinancing of existing SLL portfolios
Transition Bond,2,Corporate,Limited,Early capability; growing
Sustainability Bond,3,Corporate,Yes,DCM; sustainability bond frameworks
Working Capital Facility,3,Corporate,Yes,Standard corporate banking
Revolving Credit Facility,3,Corporate,Yes,Standard corporate banking
Term Loan,4,Corporate,Yes,Core corporate lending
Equity Bridge,2,Infrastructure,Limited,Bridge financing for equity injections
```

- [ ] **Step 6: Commit scaffold**

```bash
git add requirements.txt config/ data/deal_economics.csv data/sector_capital_needs.csv data/bank_capabilities_template.csv
git commit -m "feat: add scaffold data files and config for commercial layer"
```

---

## Task 2: `src/constants.py` — Single Source of Truth

**Files:**
- Create: `src/constants.py`
- Test: `tests/test_commercial_layer.py` (first tests)

- [ ] **Step 1: Write the first failing tests**

Create `tests/test_commercial_layer.py`:

```python
"""Tests for the commercial decision-making layer."""
import io
import warnings

import pandas as pd
import pytest

from src.constants import (
    SUBSECTORS,
    LIFECYCLE_STAGES,
    PRODUCT_CATEGORIES,
    PRODUCT_CATEGORY_MAP,
    STAGE_VOLUME_WEIGHTS,
    validate_subsectors,
)


def test_subsectors_has_nine_entries():
    assert len(SUBSECTORS) == 9


def test_lifecycle_stages_order():
    assert LIFECYCLE_STAGES == ["Development", "Construction", "Operation", "Refinancing"]


def test_stage_volume_weights_sum_to_one():
    assert abs(sum(STAGE_VOLUME_WEIGHTS.values()) - 1.0) < 0.001


def test_all_product_categories_in_product_category_map():
    values = set(PRODUCT_CATEGORY_MAP.values())
    assert values == set(PRODUCT_CATEGORIES)


def test_validate_subsectors_passes_on_valid():
    df = pd.DataFrame({"subsector": SUBSECTORS})
    validate_subsectors(df, "subsector")  # should not raise


def test_validate_subsectors_raises_on_unknown():
    df = pd.DataFrame({"subsector": ["Solar Utility-Scale", "Nonexistent Sector"]})
    with pytest.raises(ValueError, match="Nonexistent Sector"):
        validate_subsectors(df, "subsector")


def test_validate_subsectors_raises_on_nan():
    df = pd.DataFrame({"subsector": ["Solar Utility-Scale", None]})
    with pytest.raises(ValueError):
        validate_subsectors(df, "subsector")
```

- [ ] **Step 2: Run tests to confirm they fail**

```bash
pytest tests/test_commercial_layer.py -v 2>&1 | head -30
```
Expected: `ModuleNotFoundError` or `ImportError` — constants.py does not exist yet.

- [ ] **Step 3: Implement `src/constants.py`**

```python
"""Canonical strings, path constants, and cross-module utilities.

All shared identifiers live here. Import from this module — never
define subsector names, product names, or paths as raw strings elsewhere.
"""
from __future__ import annotations

import pandas as pd

# ── Canonical subsector names ─────────────────────────────────────────────
SUBSECTORS: list[str] = [
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
LIFECYCLE_STAGES: list[str] = ["Development", "Construction", "Operation", "Refinancing"]

# ── Product categories for heatmap colouring ──────────────────────────────
PRODUCT_CATEGORIES: list[str] = ["Loan", "Bond", "Blended Finance", "Equity/Mezzanine"]

# ── Default fallback for client segment ───────────────────────────────────
DEFAULT_CLIENT_SEGMENT: str = "Infrastructure"

# ── Capital channel display names and CSV column mapping ──────────────────
CAPITAL_CHANNELS: list[str] = ["Bank Debt", "Bonds", "Blended/DFI", "Equity"]
CAPITAL_CHANNEL_COLS: dict[str, str] = {
    "Bank Debt":   "bank_debt_pct",
    "Bonds":       "bond_pct",
    "Blended/DFI": "grant_pct",
    "Equity":      "equity_pct",
}

# ── Stage weights for product dominance volume attribution ─────────────────
STAGE_VOLUME_WEIGHTS: dict[str, float] = {
    "Development":  0.10,
    "Construction": 0.50,
    "Operation":    0.30,
    "Refinancing":  0.10,
}

# ── Product name → PRODUCT_CATEGORY mapping ───────────────────────────────
# SLL (Sustainability-Linked Loan) classified as Loan — bank lending instrument.
PRODUCT_CATEGORY_MAP: dict[str, str] = {
    "Development Loan":           "Loan",
    "Working Capital Facility":   "Loan",
    "Green Project Finance":      "Loan",
    "SLL Refinancing":            "Loan",
    "SLL":                        "Loan",
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
SECTOR_CAPITAL_NEEDS_CSV = f"{DATA_DIR}/sector_capital_needs.csv"
PRIORITY_WEIGHTS_YAML    = f"{CONFIG_DIR}/priority_weights.yaml"
DEFAULT_BANK_PROFILE_CSV = BANK_TEMPLATE_CSV


# ── Validation helper ─────────────────────────────────────────────────────
def validate_subsectors(df: pd.DataFrame, col: str) -> None:
    """Raise ValueError if df[col] contains values not in SUBSECTORS.

    NaN values are treated as invalid. Raises with a message listing all
    unrecognised values. Does nothing if all values are valid.
    """
    valid = set(SUBSECTORS)
    bad = [v for v in df[col] if v not in valid]  # NaN not in valid set → captured
    if bad:
        raise ValueError(
            f"Unrecognised subsector values in column '{col}': {sorted(set(str(b) for b in bad))}. "
            f"Valid values: {SUBSECTORS}"
        )
```

- [ ] **Step 4: Run tests — expect pass**

```bash
pytest tests/test_commercial_layer.py -v
```
Expected: all 7 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add src/constants.py tests/test_commercial_layer.py
git commit -m "feat: add constants.py with canonical subsectors, mappings, and validate_subsectors"
```

---

## Task 3: `src/deal_economics.py`

**Files:**
- Create: `src/deal_economics.py`
- Modify: `tests/test_commercial_layer.py` (add tests)

- [ ] **Step 1: Add failing tests**

Append to `tests/test_commercial_layer.py`:

```python
from src.deal_economics import (
    load_deal_economics,
    compute_annual_financing_volume,
    compute_fee_pool,
    build_deal_economics_summary,
)


def _make_deal_df(n=1):
    """Minimal valid deal DataFrame for testing."""
    return pd.DataFrame({
        "subsector": SUBSECTORS[:n],
        "deal_archetype": ["PF"] * n,
        "deal_size_usd_mn": [200.0] * n,
        "debt_pct": [75.0] * n,
        "bond_pct": [20.0] * n,
        "equity_pct": [25.0] * n,
        "grant_pct": [0.0] * n,
        "arranger_fee_bps": [100.0] * n,
        "commitment_fee_bps": [50.0] * n,
        "irr_expectation_pct": [12.0] * n,
        "deal_count_annual_estimate": [10] * n,
        "notes": ["test"] * n,
    })


def test_deal_economics_fee_pool_formula():
    df = _make_deal_df(1)
    result = compute_fee_pool(df)
    # volume = 200 * 10 = 2000 USD mn
    # weighted_fee = (100 + 50) / 2 = 75 bps
    # fee_pool = 2000 * 75 / 10_000 = 15.0 USD mn
    # Note: the spec's appendix table shows "200 USD mn volume → 1.5 USD mn pool" — that
    # table has a typo (assumes deal_count=1). The formula and fixture here are correct.
    assert abs(result.iloc[0]["fee_pool_usd_mn"] - 15.0) < 0.01


def test_deal_economics_volume_formula():
    df = _make_deal_df(1)
    result = compute_annual_financing_volume(df)
    assert abs(result.iloc[0]["annual_volume_usd_mn"] - 2000.0) < 0.01


def test_deal_economics_returns_raw_and_summary(tmp_path):
    # Patch the default path temporarily
    import src.deal_economics as de
    original = de.DEAL_ECONOMICS_CSV
    de.DEAL_ECONOMICS_CSV = "data/deal_economics.csv"
    raw_df, summary_df = build_deal_economics_summary(str(tmp_path / "summary.csv"))
    de.DEAL_ECONOMICS_CSV = original
    assert "bond_pct" in raw_df.columns
    assert "fee_pool_usd_mn" in summary_df.columns


def test_deal_economics_duplicate_subsector_raises():
    df = _make_deal_df(1)
    df2 = pd.concat([df, df], ignore_index=True)
    with pytest.raises(ValueError, match="duplicate"):
        from src.deal_economics import _validate_deal_df
        _validate_deal_df(df2)


def test_deal_economics_channel_pcts_sum_to_100():
    df = _make_deal_df(1)
    df.loc[0, "equity_pct"] = 99.0  # now sums to 174
    with pytest.raises(ValueError, match="100"):
        from src.deal_economics import _validate_deal_df
        _validate_deal_df(df)
```

- [ ] **Step 2: Run tests — expect fail**

```bash
pytest tests/test_commercial_layer.py::test_deal_economics_fee_pool_formula -v
```
Expected: `ModuleNotFoundError`

- [ ] **Step 3: Implement `src/deal_economics.py`**

```python
"""Deal economics layer: load deal data, compute financing volumes and fee pools."""
from __future__ import annotations

import pandas as pd

from src.constants import (
    DEAL_ECONOMICS_CSV,
    REPORTS_DIR,
    validate_subsectors,
)


def _validate_deal_df(df: pd.DataFrame) -> None:
    """Raise ValueError on invalid deal_economics DataFrame."""
    validate_subsectors(df, "subsector")
    dupes = df[df.duplicated("subsector", keep=False)]["subsector"].unique()
    if len(dupes):
        raise ValueError(f"duplicate subsector rows: {sorted(dupes)}")
    bad_sum = df[abs(df["debt_pct"] + df["equity_pct"] + df["grant_pct"] - 100) > 0.1]
    if not bad_sum.empty:
        raise ValueError(
            f"debt_pct + equity_pct + grant_pct must equal 100 (±0.1) for: "
            f"{bad_sum['subsector'].tolist()}"
        )
    bad_bond = df[df["bond_pct"] > df["debt_pct"]]
    if not bad_bond.empty:
        raise ValueError(f"bond_pct > debt_pct for: {bad_bond['subsector'].tolist()}")


def load_deal_economics(path: str = DEAL_ECONOMICS_CSV) -> pd.DataFrame:
    """Load and validate deal_economics.csv."""
    df = pd.read_csv(path)
    _validate_deal_df(df)
    return df


def compute_annual_financing_volume(df: pd.DataFrame) -> pd.DataFrame:
    """Returns DataFrame[subsector, annual_volume_usd_mn]."""
    result = df.copy()
    result["annual_volume_usd_mn"] = result["deal_size_usd_mn"] * result["deal_count_annual_estimate"]
    return result[["subsector", "annual_volume_usd_mn"]].reset_index(drop=True)


def compute_fee_pool(df: pd.DataFrame) -> pd.DataFrame:
    """Returns DataFrame[subsector, annual_volume_usd_mn, weighted_fee_bps, fee_pool_usd_mn]."""
    result = compute_annual_financing_volume(df).copy()
    result["weighted_fee_bps"] = (df["arranger_fee_bps"].values + df["commitment_fee_bps"].values) / 2
    result["fee_pool_usd_mn"] = result["annual_volume_usd_mn"] * result["weighted_fee_bps"] / 10_000
    return result.sort_values("fee_pool_usd_mn", ascending=False).reset_index(drop=True)


def build_deal_economics_summary(
    output_path: str = f"{REPORTS_DIR}/deal_economics_summary.csv",
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Load → compute volume & fee pool → write CSV.

    Returns (raw_df, summary_df).
    raw_df: all original columns from deal_economics.csv
    summary_df: subsector | annual_volume_usd_mn | weighted_fee_bps | fee_pool_usd_mn
    """
    raw_df = load_deal_economics()
    summary_df = compute_fee_pool(raw_df)
    summary_df.to_csv(output_path, index=False)
    return raw_df, summary_df
```

- [ ] **Step 4: Run deal economics tests — expect pass**

```bash
pytest tests/test_commercial_layer.py -k "deal_economics" -v
```
Expected: all 5 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add src/deal_economics.py tests/test_commercial_layer.py
git commit -m "feat: add deal_economics module with volume and fee pool computation"
```

---

## Task 4: `src/sector_priority.py`

**Files:**
- Create: `src/sector_priority.py`
- Modify: `tests/test_commercial_layer.py`

- [ ] **Step 1: Add failing tests**

Append to `tests/test_commercial_layer.py`:

```python
from src.sector_priority import load_weights, score_subsectors, get_top_n, build_sector_priority_ranking


def _make_sector_needs_df():
    return pd.DataFrame({
        "subsector": SUBSECTORS,
        "financing_need_usd_bn": [18, 10, 3, 6, 4, 5, 8, 2, 12],
        "notes": ["test"] * 9,
    })


def test_sector_priority_weights_valid_passes(tmp_path):
    yaml_path = tmp_path / "weights.yaml"
    yaml_path.write_text("weights:\n  total_capital_required: 0.30\n  deal_frequency: 0.25\n  bankability: 0.25\n  fee_generation: 0.20\n")
    w = load_weights(str(yaml_path))
    assert abs(sum(w.values()) - 1.0) < 0.001


def test_sector_priority_weights_invalid_raises(tmp_path):
    yaml_path = tmp_path / "weights.yaml"
    yaml_path.write_text("weights:\n  total_capital_required: 0.50\n  deal_frequency: 0.50\n  bankability: 0.50\n  fee_generation: 0.50\n")
    with pytest.raises(ValueError, match="sum"):
        load_weights(str(yaml_path))


def test_sector_priority_weights_missing_file_warns(tmp_path):
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        result = load_weights(str(tmp_path / "nonexistent.yaml"))
    assert any("not found" in str(x.message).lower() for x in w)
    assert abs(sum(result.values()) - 1.0) < 0.001


def test_sector_priority_top5_returns_five():
    df = pd.DataFrame({"weighted_score": range(9), "score_capital": range(9), "subsector": SUBSECTORS})
    result = get_top_n(df, 5)
    assert len(result) == 5


def test_sector_priority_fewer_than_n_ok():
    df = pd.DataFrame({"weighted_score": [1, 2, 3], "score_capital": [1, 2, 3], "subsector": SUBSECTORS[:3]})
    result = get_top_n(df, 5)
    assert len(result) == 3


def test_score_subsectors_output_columns():
    # Uses in-memory fixtures only — no disk reads, no writes to reports/
    from src.deal_economics import compute_fee_pool
    needs = _make_sector_needs_df()
    deal_df = pd.DataFrame({
        "subsector": SUBSECTORS,
        "deal_size_usd_mn": [150.0] * 9,
        "deal_count_annual_estimate": [10] * 9,
        "arranger_fee_bps": [100.0] * 9,
        "commitment_fee_bps": [50.0] * 9,
    })
    summary = compute_fee_pool(deal_df)  # produces fee_pool_usd_mn without hitting disk
    weights = {"total_capital_required": 0.30, "deal_frequency": 0.25, "bankability": 0.25, "fee_generation": 0.20}
    scored = score_subsectors(needs, deal_df, summary, weights)
    for col in ["subsector", "score_capital", "score_frequency", "score_bankability", "score_fee", "weighted_score", "rank", "top5_flag"]:
        assert col in scored.columns
    assert scored["top5_flag"].sum() == 5
```

- [ ] **Step 2: Run — expect fail**

```bash
pytest tests/test_commercial_layer.py -k "sector_priority or score_subsectors" -v 2>&1 | head -20
```

- [ ] **Step 3: Implement `src/sector_priority.py`**

```python
"""Sector prioritisation model: score and rank subsectors for bank strategy focus."""
from __future__ import annotations

import warnings
from pathlib import Path

import pandas as pd
import yaml

from src.constants import (
    BANKABILITY_SCORES := {
        "Solar Utility-Scale":        5,
        "Wind Onshore":               4,
        "Wind Offshore":              2,
        "Battery Storage":            3,
        "EV Charging Infrastructure": 2,
        "Green Buildings":            3,
        "Industrial Decarbonisation": 3,
        "Circular Economy":           2,
        "Transmission & Grid":        4,
    },
    PRIORITY_WEIGHTS_YAML,
    REPORTS_DIR,
    SECTOR_CAPITAL_NEEDS_CSV,
    validate_subsectors,
)
```

Wait — Python does not support `:=` in import statements. Write the file properly:

```python
"""Sector prioritisation model: score and rank subsectors for bank strategy focus."""
from __future__ import annotations

import warnings
from pathlib import Path

import pandas as pd
import yaml

from src.constants import (
    PRIORITY_WEIGHTS_YAML,
    REPORTS_DIR,
    SECTOR_CAPITAL_NEEDS_CSV,
    validate_subsectors,
)
from src.deal_economics import build_deal_economics_summary, load_deal_economics

# ── Scoring thresholds ────────────────────────────────────────────────────
# (min_value_inclusive, score) — first matching threshold wins
CAPITAL_THRESHOLDS = [(50, 5), (20, 4), (10, 3), (5, 2), (0, 1)]
FREQUENCY_THRESHOLDS = [(20, 5), (10, 4), (5, 3), (2, 2), (0, 1)]
FEE_THRESHOLDS = [(50, 5), (20, 4), (10, 3), (5, 2), (0, 1)]

BANKABILITY_SCORES: dict[str, int] = {
    "Solar Utility-Scale":        5,
    "Wind Onshore":               4,
    "Wind Offshore":              2,
    "Battery Storage":            3,
    "EV Charging Infrastructure": 2,
    "Green Buildings":            3,
    "Industrial Decarbonisation": 3,
    "Circular Economy":           2,
    "Transmission & Grid":        4,
}

DEFAULT_WEIGHTS: dict[str, float] = {
    "total_capital_required": 0.30,
    "deal_frequency":         0.25,
    "bankability":            0.25,
    "fee_generation":         0.20,
}


def _score_from_thresholds(value: float, thresholds: list[tuple[float, int]]) -> int:
    for min_val, score in thresholds:
        if value >= min_val:
            return score
    return 1


def load_sector_capital_needs(path: str = SECTOR_CAPITAL_NEEDS_CSV) -> pd.DataFrame:
    """Load sector_capital_needs.csv. Raises on unknown subsectors or missing columns."""
    df = pd.read_csv(path)
    for col in ("subsector", "financing_need_usd_bn"):
        if col not in df.columns:
            raise ValueError(f"Missing required column '{col}' in {path}")
    validate_subsectors(df, "subsector")
    return df


def load_weights(config_path: str = PRIORITY_WEIGHTS_YAML) -> dict[str, float]:
    """Load YAML weights. Warns and returns defaults if file not found."""
    if not Path(config_path).exists():
        warnings.warn(f"Config {config_path} not found; using default weights.", stacklevel=2)
        return dict(DEFAULT_WEIGHTS)
    with open(config_path) as f:
        data = yaml.safe_load(f)
    w = data.get("weights", {})
    total = sum(w.values())
    if abs(total - 1.0) > 0.001:
        raise ValueError(f"Weights must sum to 1.0 (got {total:.4f})")
    return w


def score_subsectors(
    sector_needs_df: pd.DataFrame,
    raw_deal_df: pd.DataFrame,
    summary_deal_df: pd.DataFrame,
    weights: dict[str, float],
) -> pd.DataFrame:
    """Score each subsector 1–5 on four dimensions and return ranked DataFrame."""
    rows = []
    for sub in sector_needs_df["subsector"]:
        need = sector_needs_df.loc[sector_needs_df["subsector"] == sub, "financing_need_usd_bn"].iloc[0]
        freq = raw_deal_df.loc[raw_deal_df["subsector"] == sub, "deal_count_annual_estimate"].iloc[0]
        fee  = summary_deal_df.loc[summary_deal_df["subsector"] == sub, "fee_pool_usd_mn"].iloc[0] if sub in summary_deal_df["subsector"].values else 0.0

        sc = _score_from_thresholds(need, CAPITAL_THRESHOLDS)
        sf = _score_from_thresholds(freq, FREQUENCY_THRESHOLDS)
        sb = BANKABILITY_SCORES.get(sub, 1)
        se = _score_from_thresholds(fee, FEE_THRESHOLDS)

        ws = (sc * weights["total_capital_required"] +
              sf * weights["deal_frequency"] +
              sb * weights["bankability"] +
              se * weights["fee_generation"])
        rows.append({"subsector": sub, "score_capital": sc, "score_frequency": sf,
                     "score_bankability": sb, "score_fee": se, "weighted_score": round(ws, 4)})

    df = pd.DataFrame(rows)
    df = df.sort_values(["weighted_score", "score_capital"], ascending=False).reset_index(drop=True)
    df["rank"] = range(1, len(df) + 1)
    df["top5_flag"] = df["rank"] <= 5
    return df


def get_top_n(scored_df: pd.DataFrame, n: int = 5) -> pd.DataFrame:
    """Return top-N rows by weighted_score; ties broken by score_capital."""
    return scored_df.sort_values(
        ["weighted_score", "score_capital"], ascending=False
    ).head(n).reset_index(drop=True)


def build_sector_priority_ranking(
    output_path: str = f"{REPORTS_DIR}/sector_priority_ranking.csv",
) -> pd.DataFrame:
    """Self-contained orchestration: load all inputs, score, write CSV, return DataFrame."""
    import os
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    needs      = load_sector_capital_needs()
    raw_df     = load_deal_economics()
    _, summary = build_deal_economics_summary()
    weights    = load_weights()
    scored     = score_subsectors(needs, raw_df, summary, weights)
    scored.to_csv(output_path, index=False)
    return scored
```

- [ ] **Step 4: Run sector priority tests — expect pass**

```bash
pytest tests/test_commercial_layer.py -k "sector_priority or score_subsectors or weights" -v
```
Expected: all 7 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add src/sector_priority.py tests/test_commercial_layer.py
git commit -m "feat: add sector_priority module — scoring, ranking, configurable weights"
```

---

## Task 5: `src/lifecycle.py`

**Files:**
- Create: `src/lifecycle.py`
- Modify: `tests/test_commercial_layer.py`

- [ ] **Step 1: Add failing tests**

Append to `tests/test_commercial_layer.py`:

```python
from src.lifecycle import build_lifecycle_matrix, export_lifecycle_matrix


def test_lifecycle_matrix_covers_all_subsectors():
    df = build_lifecycle_matrix()
    assert set(df["subsector"].unique()) == set(SUBSECTORS)
    assert set(df["stage"].unique()) == set(LIFECYCLE_STAGES)
    # Every subsector must have all 4 stages
    for sub in SUBSECTORS:
        stages = df[df["subsector"] == sub]["stage"].tolist()
        assert set(stages) == set(LIFECYCLE_STAGES), f"Missing stages for {sub}"


def test_lifecycle_matrix_products_in_category_map():
    df = build_lifecycle_matrix()
    for col in ("primary_product", "secondary_product"):
        unknown = set(df[col]) - set(PRODUCT_CATEGORY_MAP.keys())
        assert not unknown, f"Products not in PRODUCT_CATEGORY_MAP ({col}): {unknown}"


def test_export_lifecycle_matrix_writes_file(tmp_path):
    out = str(tmp_path / "matrix.csv")
    df = export_lifecycle_matrix(output_path=out)
    import os
    assert os.path.exists(out)
    assert len(df) == len(SUBSECTORS) * len(LIFECYCLE_STAGES)
```

- [ ] **Step 2: Run — expect fail**

```bash
pytest tests/test_commercial_layer.py -k "lifecycle" -v 2>&1 | head -10
```

- [ ] **Step 3: Implement `src/lifecycle.py`**

```python
"""Lifecycle financing model: product evolution across development stages."""
from __future__ import annotations

import pandas as pd

from src.constants import (
    LIFECYCLE_STAGES,
    PRODUCT_CATEGORY_MAP,
    REPORTS_DIR,
    SUBSECTORS,
)

LIFECYCLE_DATA: dict[str, dict[str, dict[str, str]]] = {
    "Solar Utility-Scale": {
        "Development":  {"primary": "Development Loan",      "secondary": "Equity Bridge",            "rationale": "Pre-PPA risk; short-tenor development facility"},
        "Construction": {"primary": "Green Project Finance", "secondary": "Blended Finance",          "rationale": "Senior secured; DFI co-lending common at scale"},
        "Operation":    {"primary": "Green Bond",            "secondary": "SLL Refinancing",          "rationale": "Stable cashflow enables bond market access"},
        "Refinancing":  {"primary": "SLL Refinancing",       "secondary": "Green Bond Tap",           "rationale": "Rate optimisation; ESG KPI linkage adds pricing benefit"},
    },
    "Wind Onshore": {
        "Development":  {"primary": "Development Loan",      "secondary": "Equity Bridge",            "rationale": "Site development and permitting phase"},
        "Construction": {"primary": "Green Project Finance", "secondary": "DFI Co-lending",           "rationale": "Senior secured; multilateral co-lending available"},
        "Operation":    {"primary": "Green Bond",            "secondary": "Term Loan",                "rationale": "Long-tenor stable cashflow; bond execution viable"},
        "Refinancing":  {"primary": "SLL Refinancing",       "secondary": "Green Bond Tap",           "rationale": "Optimise cost of capital with sustainability linkage"},
    },
    "Wind Offshore": {
        "Development":  {"primary": "Development Loan",      "secondary": "Mezzanine Loan",           "rationale": "High complexity; mezzanine often required for risk layering"},
        "Construction": {"primary": "Blended Finance",       "secondary": "Green Project Finance",    "rationale": "Nascent market; concessional capital essential"},
        "Operation":    {"primary": "Green Project Finance", "secondary": "Green Bond",               "rationale": "Track record builds before bond market access"},
        "Refinancing":  {"primary": "Green Bond",            "secondary": "SLL Refinancing",          "rationale": "Refinancing onto bond market as asset class matures"},
    },
    "Battery Storage": {
        "Development":  {"primary": "Development Loan",      "secondary": "Equity Bridge",            "rationale": "Technology and offtake risk managed at development stage"},
        "Construction": {"primary": "Green Project Finance", "secondary": "Partial Credit Guarantee", "rationale": "PCG from DFIs increasingly used to enhance bankability"},
        "Operation":    {"primary": "SLL",                   "secondary": "Green Bond",               "rationale": "SLL suitable given measurable storage/grid KPIs"},
        "Refinancing":  {"primary": "Green Bond",            "secondary": "SLL Refinancing",          "rationale": "Bond market access as storage asset class matures"},
    },
    "EV Charging Infrastructure": {
        "Development":  {"primary": "Working Capital Facility", "secondary": "Development Loan",      "rationale": "Fragmented, asset-light; working capital more relevant"},
        "Construction": {"primary": "Green Project Finance",    "secondary": "Blended Finance",       "rationale": "Anchor sites project-financed; DFI support for network buildout"},
        "Operation":    {"primary": "SLL",                      "secondary": "Revolving Credit Facility", "rationale": "SLL with utilisation/uptime KPIs"},
        "Refinancing":  {"primary": "Sustainability Bond",      "secondary": "SLL Refinancing",       "rationale": "Portfolio aggregation enables bond market access"},
    },
    "Green Buildings": {
        "Development":  {"primary": "Development Loan",      "secondary": "Equity Bridge",            "rationale": "Developer finance at pre-construction stage"},
        "Construction": {"primary": "Green Project Finance", "secondary": "Concessional Tranche",     "rationale": "Green certification unlocks preferential pricing"},
        "Operation":    {"primary": "Sustainability Bond",   "secondary": "SLL",                      "rationale": "Portfolio of certified buildings suitable for sustainability bond"},
        "Refinancing":  {"primary": "SLL Refinancing",       "secondary": "Green Bond Tap",           "rationale": "Ongoing green certification metrics link to margin ratchets"},
    },
    "Industrial Decarbonisation": {
        "Development":  {"primary": "Working Capital Facility", "secondary": "Development Loan",      "rationale": "Technology assessment and feasibility; corporate credit-backed"},
        "Construction": {"primary": "SLL",                      "secondary": "Green Project Finance", "rationale": "SLL against decarbonisation KPIs; PF for discrete capex"},
        "Operation":    {"primary": "Transition Bond",          "secondary": "SLL",                   "rationale": "Transition bond framework appropriate for hard-to-abate sector"},
        "Refinancing":  {"primary": "Sustainability Bond",      "secondary": "SLL Refinancing",       "rationale": "Refinancing as decarbonisation pathway matures"},
    },
    "Circular Economy": {
        "Development":  {"primary": "Development Loan",      "secondary": "Concessional Tranche",     "rationale": "Thin track record; concessional tranche often needed"},
        "Construction": {"primary": "Blended Finance",       "secondary": "Green Project Finance",    "rationale": "DFI/blended finance essential given nascent viability"},
        "Operation":    {"primary": "Green Bond",            "secondary": "SLL",                      "rationale": "Operating asset; green bond if use-of-proceeds clear"},
        "Refinancing":  {"primary": "SLL Refinancing",       "secondary": "Sustainability Bond",      "rationale": "SLL with circularity metrics for refinancing phase"},
    },
    "Transmission & Grid": {
        "Development":  {"primary": "Development Loan",      "secondary": "Guarantee",                "rationale": "Regulated utility; government guarantee reduces dev debt cost"},
        "Construction": {"primary": "Green Project Finance", "secondary": "DFI Co-lending",           "rationale": "Large-ticket senior secured; multilateral co-lending common"},
        "Operation":    {"primary": "Green Bond",            "secondary": "Sustainability Bond",      "rationale": "Regulated cashflow ideal for long-duration bond"},
        "Refinancing":  {"primary": "Green Bond Tap",        "secondary": "SLL Refinancing",          "rationale": "Tap existing green bond programme; SLL where grid KPIs measurable"},
    },
}


def build_lifecycle_matrix() -> pd.DataFrame:
    """Returns DataFrame[subsector, stage, primary_product, secondary_product, rationale].

    Validates:
    - All SUBSECTORS present
    - All LIFECYCLE_STAGES present per subsector
    - All product strings exist in PRODUCT_CATEGORY_MAP
    """
    rows = []
    for sub in SUBSECTORS:
        for stage in LIFECYCLE_STAGES:
            cell = LIFECYCLE_DATA[sub][stage]
            rows.append({
                "subsector":        sub,
                "stage":            stage,
                "primary_product":  cell["primary"],
                "secondary_product": cell["secondary"],
                "rationale":        cell["rationale"],
            })

    df = pd.DataFrame(rows)

    # Validate all products in PRODUCT_CATEGORY_MAP
    for col in ("primary_product", "secondary_product"):
        unknown = set(df[col]) - set(PRODUCT_CATEGORY_MAP.keys())
        if unknown:
            raise ValueError(f"Products not in PRODUCT_CATEGORY_MAP ({col}): {unknown}")

    return df


def export_lifecycle_matrix(
    output_path: str = f"{REPORTS_DIR}/lifecycle_financing_matrix.csv",
) -> pd.DataFrame:
    """Write lifecycle matrix to CSV and return DataFrame."""
    df = build_lifecycle_matrix()
    df.to_csv(output_path, index=False)
    return df
```

- [ ] **Step 4: Run lifecycle tests — expect pass**

```bash
pytest tests/test_commercial_layer.py -k "lifecycle" -v
```
Expected: all 3 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add src/lifecycle.py tests/test_commercial_layer.py
git commit -m "feat: add lifecycle module — full 9-subsector × 4-stage product matrix"
```

---

## Task 6: `src/bank_strategy.py`

**Files:**
- Create: `src/bank_strategy.py`
- Modify: `tests/test_commercial_layer.py`

- [ ] **Step 1: Add failing tests**

Append to `tests/test_commercial_layer.py`:

```python
from src.bank_strategy import (
    load_bank_profile,
    map_capabilities_to_sectors,
    get_top_strategic_plays,
    get_product_mix_recommendation,
    get_client_targeting_strategy,
    build_bank_strategy_output,
)
from src.lifecycle import build_lifecycle_matrix, export_lifecycle_matrix
from src.sector_priority import build_sector_priority_ranking, get_top_n


def _make_capabilities_df():
    return pd.DataFrame({
        "capability": ["Green Project Finance", "SLL", "Green Bond"],
        "strength": [4, 3, 2],
        "client_segment": ["Infrastructure", "Corporate", "Corporate"],
        "india_presence": ["Yes", "Yes", "Yes"],
        "notes": ["", "", ""],
    })


def test_bank_strategy_plays_columns():
    lifecycle = build_lifecycle_matrix()
    priority = build_sector_priority_ranking()
    top5 = get_top_n(priority, 5)
    caps = _make_capabilities_df()
    mapped = map_capabilities_to_sectors(caps, top5, lifecycle)
    plays = get_top_strategic_plays(mapped)
    for col in ["rank", "subsector", "stage", "recommended_action", "fit_score_normalised"]:
        assert col in plays.columns


def test_bank_strategy_zero_fit_equal_allocation():
    lifecycle = build_lifecycle_matrix()
    caps = pd.DataFrame({
        "capability": ["Unknown Product"],
        "strength": [5],
        "client_segment": ["Corporate"],
        "india_presence": ["Yes"],
        "notes": [""],
    })
    priority = build_sector_priority_ranking()
    top5 = get_top_n(priority, 5)
    mapped = map_capabilities_to_sectors(caps, top5, lifecycle)
    mix = get_product_mix_recommendation(mapped)
    for pct in mix["recommended_allocation_pct"]:
        assert abs(pct - 25.0) < 0.01


def test_bank_strategy_tiebreak_uses_lifecycle_order():
    # Two subsectors, all stages tied at fit_score_normalised=2.0
    # Tiebreak must resolve to "Development" (first in LIFECYCLE_STAGES) for both
    rows = []
    for sub in ["Solar Utility-Scale", "Wind Onshore"]:
        for stage in LIFECYCLE_STAGES:
            rows.append({
                "subsector": sub, "stage": stage,
                "primary_product": "Green Bond", "secondary_product": "SLL Refinancing",
                "primary_strength": 3, "secondary_strength": 0,
                "fit_score": 3.0, "fit_score_normalised": 2.0,
            })
    mapped = pd.DataFrame(rows)
    caps = _make_capabilities_df()
    result = get_client_targeting_strategy(mapped, caps)
    for sub in ["Solar Utility-Scale", "Wind Onshore"]:
        row = result[result["subsector"] == sub]
        assert row.iloc[0]["entry_stage"] == "Development", (
            f"Expected Development for {sub} (first in LIFECYCLE_STAGES), "
            f"got {row.iloc[0]['entry_stage']}"
        )


def test_bank_strategy_three_csvs_written(tmp_path):
    plays_path   = str(tmp_path / "plays.csv")
    mix_path     = str(tmp_path / "mix.csv")
    target_path  = str(tmp_path / "targeting.csv")
    build_bank_strategy_output(
        plays_path=plays_path, mix_path=mix_path, targeting_path=target_path
    )
    import os
    for p in [plays_path, mix_path, target_path]:
        assert os.path.exists(p) and os.path.getsize(p) > 0


def test_bank_strategy_empty_priority_raises():
    lifecycle = build_lifecycle_matrix()
    empty = pd.DataFrame(columns=["subsector", "weighted_score", "score_capital",
                                   "score_frequency", "score_bankability", "score_fee",
                                   "rank", "top5_flag"])
    with pytest.raises(ValueError, match="No subsectors"):
        build_bank_strategy_output(priority_df=empty, lifecycle_df=lifecycle)
```

- [ ] **Step 2: Run — expect fail**

```bash
pytest tests/test_commercial_layer.py -k "bank_strategy" -v 2>&1 | head -15
```

- [ ] **Step 3: Implement `src/bank_strategy.py`**

```python
"""Bank strategy engine: map bank capabilities to sector opportunities."""
from __future__ import annotations

import pandas as pd

from src.constants import (
    DEFAULT_BANK_PROFILE_CSV,
    DEFAULT_CLIENT_SEGMENT,
    LIFECYCLE_STAGES,
    PRODUCT_CATEGORIES,
    PRODUCT_CATEGORY_MAP,
    REPORTS_DIR,
)


def load_bank_profile(path: str = DEFAULT_BANK_PROFILE_CSV) -> pd.DataFrame:
    """Load bank capabilities CSV. Validates required columns."""
    df = pd.read_csv(path)
    for col in ("capability", "strength", "client_segment", "india_presence"):
        if col not in df.columns:
            raise ValueError(f"Missing required column '{col}' in {path}")
    return df


def _lookup_strength(capabilities_df: pd.DataFrame, product: str) -> float:
    """Case-insensitive match; returns max strength or 0."""
    folded = product.casefold()
    matches = capabilities_df[capabilities_df["capability"].str.casefold() == folded]
    if matches.empty:
        return 0.0
    return float(matches["strength"].max())


def map_capabilities_to_sectors(
    capabilities_df: pd.DataFrame,
    priority_df: pd.DataFrame,
    lifecycle_df: pd.DataFrame,
) -> pd.DataFrame:
    """Cross-map bank capabilities against top-N sectors × lifecycle stages."""
    rows = []
    for _, p_row in priority_df.iterrows():
        sub = p_row["subsector"]
        sub_lc = lifecycle_df[lifecycle_df["subsector"] == sub]
        for _, lc_row in sub_lc.iterrows():
            ps = _lookup_strength(capabilities_df, lc_row["primary_product"])
            ss = _lookup_strength(capabilities_df, lc_row["secondary_product"])
            fit = ps + 0.5 * ss
            fit_norm = round(fit / 7.5 * 5, 2)
            rows.append({
                "subsector":           sub,
                "stage":               lc_row["stage"],
                "primary_product":     lc_row["primary_product"],
                "secondary_product":   lc_row["secondary_product"],
                "primary_strength":    ps,
                "secondary_strength":  ss,
                "fit_score":           fit,
                "fit_score_normalised": fit_norm,
            })
    return pd.DataFrame(rows)


def get_top_strategic_plays(mapped_df: pd.DataFrame) -> pd.DataFrame:
    """Return ranked strategic plays with recommended action."""
    df = mapped_df.copy().sort_values("fit_score_normalised", ascending=False).reset_index(drop=True)
    df["rank"] = range(1, len(df) + 1)

    def _action(score: float) -> str:
        if score >= 4.0:
            return "Lead Arranger"
        if score >= 2.5:
            return "Co-Arranger"
        return "Build Capability / Partner"

    df["recommended_action"] = df["fit_score_normalised"].apply(_action)
    return df[["rank", "subsector", "stage", "recommended_action", "fit_score_normalised"]]


def get_product_mix_recommendation(mapped_df: pd.DataFrame) -> pd.DataFrame:
    """Return % allocation across PRODUCT_CATEGORIES. Equal split if all scores zero."""
    cat_scores: dict[str, float] = {cat: 0.0 for cat in PRODUCT_CATEGORIES}
    for _, row in mapped_df.iterrows():
        cat = PRODUCT_CATEGORY_MAP.get(row["primary_product"])
        if cat:
            cat_scores[cat] += row["fit_score_normalised"]
    total = sum(cat_scores.values())
    rows = []
    for cat, score in cat_scores.items():
        pct = (score / total * 100) if total > 0 else 25.0
        rows.append({"product_category": cat, "total_fit_score": score, "recommended_allocation_pct": round(pct, 2)})
    return pd.DataFrame(rows)


def get_client_targeting_strategy(
    mapped_df: pd.DataFrame,
    capabilities_df: pd.DataFrame,
) -> pd.DataFrame:
    """Return entry point per subsector with client segment and rationale."""
    stage_order = {s: i for i, s in enumerate(LIFECYCLE_STAGES)}
    rows = []
    for sub in mapped_df["subsector"].unique():
        sub_df = mapped_df[mapped_df["subsector"] == sub].copy()
        sub_df["_stage_order"] = sub_df["stage"].map(stage_order)
        best = sub_df.sort_values(
            ["fit_score_normalised", "_stage_order"], ascending=[False, True]
        ).iloc[0]

        product = best["primary_product"]
        folded = product.casefold()
        matches = capabilities_df[capabilities_df["capability"].str.casefold() == folded]
        if matches.empty:
            segment = DEFAULT_CLIENT_SEGMENT
        else:
            segment = matches.sort_values("strength", ascending=False).iloc[0]["client_segment"]

        rows.append({
            "subsector":      sub,
            "client_segment": segment,
            "entry_stage":    best["stage"],
            "entry_point":    product,
            "rationale":      f"Highest capability fit at {best['stage']} stage (score {best['fit_score_normalised']})",
        })
    return pd.DataFrame(rows)


def build_bank_strategy_output(
    bank_profile_path: str = DEFAULT_BANK_PROFILE_CSV,
    priority_df: "pd.DataFrame | None" = None,
    lifecycle_df: "pd.DataFrame | None" = None,
    n_sectors: int = 5,
    plays_path: str = f"{REPORTS_DIR}/bank_strategy_plays.csv",
    mix_path:   str = f"{REPORTS_DIR}/bank_strategy_product_mix.csv",
    targeting_path: str = f"{REPORTS_DIR}/bank_strategy_targeting.csv",
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Orchestrate full bank strategy output. Returns (plays, mix, targeting)."""
    from src.lifecycle import export_lifecycle_matrix
    from src.sector_priority import build_sector_priority_ranking, get_top_n

    capabilities = load_bank_profile(bank_profile_path)
    if priority_df is None:
        priority_df = build_sector_priority_ranking()
    if lifecycle_df is None:
        lifecycle_df = export_lifecycle_matrix()

    top_n = get_top_n(priority_df, n_sectors)
    if len(top_n) == 0:
        raise ValueError("No subsectors to map — check sector_priority output.")

    mapped    = map_capabilities_to_sectors(capabilities, top_n, lifecycle_df)
    plays     = get_top_strategic_plays(mapped)
    mix       = get_product_mix_recommendation(mapped)
    targeting = get_client_targeting_strategy(mapped, capabilities)

    plays.to_csv(plays_path, index=False)
    mix.to_csv(mix_path, index=False)
    targeting.to_csv(targeting_path, index=False)
    return plays, mix, targeting
```

- [ ] **Step 4: Run bank strategy tests — expect pass**

```bash
pytest tests/test_commercial_layer.py -k "bank_strategy" -v
```
Expected: all 5 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add src/bank_strategy.py tests/test_commercial_layer.py
git commit -m "feat: add bank_strategy engine — generic capability mapping and strategic plays"
```

---

## Task 7: New Figure Functions in `src/figures.py`

**Files:**
- Modify: `src/figures.py` (append only — existing functions untouched)
- Modify: `tests/test_commercial_layer.py`

- [ ] **Step 1: Add smoke tests for figures**

Append to `tests/test_commercial_layer.py`:

```python
import os
from src.deal_economics import load_deal_economics, compute_annual_financing_volume
from src.lifecycle import build_lifecycle_matrix
from src.bank_strategy import map_capabilities_to_sectors
from src.sector_priority import build_sector_priority_ranking, get_top_n

# Import new figure functions (appended to existing figures.py)
from src.figures import (
    plot_capital_allocation_by_sector,
    plot_product_dominance_by_sector,
    plot_lifecycle_heatmap,
    plot_bank_opportunity_heatmap,
)


def test_plot_capital_allocation_creates_file(tmp_path):
    raw_df = load_deal_economics()
    vol_df = compute_annual_financing_volume(raw_df)
    out = str(tmp_path / "capital.png")
    plot_capital_allocation_by_sector(vol_df, raw_df, output_path=out)
    assert os.path.exists(out) and os.path.getsize(out) > 0


def test_plot_product_dominance_creates_file(tmp_path):
    raw_df = load_deal_economics()
    lifecycle = build_lifecycle_matrix()
    out = str(tmp_path / "dominance.png")
    plot_product_dominance_by_sector(lifecycle, raw_df, output_path=out)
    assert os.path.exists(out) and os.path.getsize(out) > 0


def test_plot_lifecycle_heatmap_creates_file(tmp_path):
    lifecycle = build_lifecycle_matrix()
    out = str(tmp_path / "lifecycle.png")
    plot_lifecycle_heatmap(lifecycle, output_path=out)
    assert os.path.exists(out) and os.path.getsize(out) > 0


def test_plot_bank_opportunity_heatmap_creates_file(tmp_path):
    lifecycle = build_lifecycle_matrix()
    priority = build_sector_priority_ranking()
    top5 = get_top_n(priority, 5)
    caps = load_bank_profile()
    mapped = map_capabilities_to_sectors(caps, top5, lifecycle)
    out = str(tmp_path / "bank.png")
    plot_bank_opportunity_heatmap(mapped, output_path=out)
    assert os.path.exists(out) and os.path.getsize(out) > 0
```

- [ ] **Step 2: Run — expect fail (functions not defined yet)**

```bash
pytest tests/test_commercial_layer.py -k "plot_" -v 2>&1 | head -10
```

- [ ] **Step 3: Read existing `src/figures.py` to find the end of the file**

```bash
tail -10 src/figures.py
```

Note the last line number and the existing styling conventions (font, DPI, figure size).

- [ ] **Step 4: Append new figure functions to `src/figures.py`**

Add after the last existing function — do not modify any existing code:

```python

# ════════════════════════════════════════════════════════════════════════════
# COMMERCIAL LAYER — new figure functions (appended; existing code untouched)
# ════════════════════════════════════════════════════════════════════════════


def plot_capital_allocation_by_sector(
    volume_df: "pd.DataFrame",
    raw_deal_df: "pd.DataFrame",
    output_path: str = "figures/capital_allocation_by_sector.png",
) -> None:
    """Horizontal stacked bar: annual financing volume by subsector, stacked by capital channel."""
    import matplotlib.pyplot as plt
    import numpy as np
    from src.constants import CAPITAL_CHANNELS, SUBSECTORS

    merged = volume_df.merge(raw_deal_df[["subsector", "debt_pct", "bond_pct", "equity_pct", "grant_pct"]], on="subsector")

    # Compute per-channel volumes (USD mn)
    merged["Bank Debt"]   = merged["annual_volume_usd_mn"] * (merged["debt_pct"] - merged["bond_pct"]) / 100
    merged["Bonds"]       = merged["annual_volume_usd_mn"] * merged["bond_pct"] / 100
    merged["Blended/DFI"] = merged["annual_volume_usd_mn"] * merged["grant_pct"] / 100
    merged["Equity"]      = merged["annual_volume_usd_mn"] * merged["equity_pct"] / 100

    # Sort by total volume descending
    merged = merged.sort_values("annual_volume_usd_mn", ascending=True)

    fig, ax = plt.subplots(figsize=(12, 7))
    colours = {"Bank Debt": "#2166ac", "Bonds": "#1a9641", "Blended/DFI": "#f46d43", "Equity": "#762a83"}
    lefts = np.zeros(len(merged))
    for channel in CAPITAL_CHANNELS:
        values = merged[channel].values
        ax.barh(merged["subsector"], values, left=lefts, color=colours[channel], label=channel)
        lefts += values

    ax.set_xlabel("Annual Financing Volume (USD mn)", fontname="DejaVu Sans")
    ax.set_title("Capital Allocation by Sector", fontname="DejaVu Sans", fontweight="bold")
    ax.legend(loc="lower right", fontsize=9)
    plt.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)


def plot_product_dominance_by_sector(
    lifecycle_df: "pd.DataFrame",
    raw_deal_df: "pd.DataFrame",
    output_path: str = "figures/product_dominance_by_sector.png",
) -> None:
    """Heatmap: subsectors × PRODUCT_CATEGORIES, intensity = stage-weighted volume."""
    import matplotlib.pyplot as plt
    import numpy as np
    from src.constants import PRODUCT_CATEGORIES, PRODUCT_CATEGORY_MAP, STAGE_VOLUME_WEIGHTS, SUBSECTORS

    vol = raw_deal_df[["subsector", "deal_size_usd_mn", "deal_count_annual_estimate"]].copy()
    vol["annual_volume_usd_mn"] = vol["deal_size_usd_mn"] * vol["deal_count_annual_estimate"]

    merged = lifecycle_df.merge(vol[["subsector", "annual_volume_usd_mn"]], on="subsector")
    merged["stage_volume"] = merged["annual_volume_usd_mn"] * merged["stage"].map(STAGE_VOLUME_WEIGHTS)
    merged["product_category"] = merged["primary_product"].map(PRODUCT_CATEGORY_MAP)

    pivot = merged.groupby(["subsector", "product_category"])["stage_volume"].sum().unstack(fill_value=0)
    # Ensure all categories present
    for cat in PRODUCT_CATEGORIES:
        if cat not in pivot.columns:
            pivot[cat] = 0
    pivot = pivot[PRODUCT_CATEGORIES].reindex(SUBSECTORS)

    fig, ax = plt.subplots(figsize=(12, 7))
    im = ax.imshow(pivot.values, aspect="auto", cmap="YlOrRd")
    ax.set_xticks(range(len(PRODUCT_CATEGORIES)))
    ax.set_xticklabels(PRODUCT_CATEGORIES, fontname="DejaVu Sans")
    ax.set_yticks(range(len(SUBSECTORS)))
    ax.set_yticklabels(SUBSECTORS, fontname="DejaVu Sans")
    plt.colorbar(im, ax=ax, label="Stage-weighted Volume (USD mn)")
    ax.set_title("Product Dominance by Sector", fontname="DejaVu Sans", fontweight="bold")
    fig.text(0.5, 0.01, "Note: SLL classified as Loan (bank lending instrument).",
             ha="center", fontsize=8, style="italic")
    plt.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)


def plot_lifecycle_heatmap(
    matrix_df: "pd.DataFrame",
    output_path: str = "figures/lifecycle_financing_flow.png",
) -> None:
    """Heatmap: subsectors × lifecycle stages, colour = primary product category."""
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    import numpy as np
    from src.constants import LIFECYCLE_STAGES, PRODUCT_CATEGORY_MAP, SUBSECTORS

    CAT_COLOURS = {
        "Loan":             "#2166ac",
        "Bond":             "#1a9641",
        "Blended Finance":  "#f46d43",
        "Equity/Mezzanine": "#762a83",
    }

    pivot = matrix_df.pivot(index="subsector", columns="stage", values="primary_product")
    pivot = pivot.reindex(index=SUBSECTORS, columns=LIFECYCLE_STAGES)

    fig, ax = plt.subplots(figsize=(12, 7))
    for row_i, sub in enumerate(SUBSECTORS):
        for col_i, stage in enumerate(LIFECYCLE_STAGES):
            product = pivot.loc[sub, stage]
            cat = PRODUCT_CATEGORY_MAP.get(product, "Loan")
            colour = CAT_COLOURS[cat]
            ax.add_patch(plt.Rectangle((col_i, row_i), 1, 1, color=colour, ec="white", lw=1.5))
            ax.text(col_i + 0.5, row_i + 0.5, product, ha="center", va="center",
                    fontsize=7, color="white", fontname="DejaVu Sans", wrap=True)

    ax.set_xlim(0, len(LIFECYCLE_STAGES))
    ax.set_ylim(0, len(SUBSECTORS))
    ax.set_xticks([i + 0.5 for i in range(len(LIFECYCLE_STAGES))])
    ax.set_xticklabels(LIFECYCLE_STAGES, fontname="DejaVu Sans")
    ax.set_yticks([i + 0.5 for i in range(len(SUBSECTORS))])
    ax.set_yticklabels(SUBSECTORS, fontname="DejaVu Sans")
    ax.set_title("Lifecycle Financing Flow by Subsector", fontname="DejaVu Sans", fontweight="bold")

    legend_patches = [mpatches.Patch(color=c, label=l) for l, c in CAT_COLOURS.items()]
    ax.legend(handles=legend_patches, loc="upper right", fontsize=8)
    plt.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)


def plot_bank_opportunity_heatmap(
    mapped_df: "pd.DataFrame",
    output_path: str = "figures/bank_opportunity_heatmap.png",
) -> None:
    """Heatmap: top sectors × lifecycle stages, intensity = bank capability fit score."""
    import matplotlib.pyplot as plt
    import numpy as np
    from src.constants import LIFECYCLE_STAGES

    subsectors = list(mapped_df["subsector"].unique())
    pivot = mapped_df.pivot(index="subsector", columns="stage", values="fit_score_normalised")
    pivot = pivot.reindex(index=subsectors, columns=LIFECYCLE_STAGES).fillna(0)

    fig, ax = plt.subplots(figsize=(12, 7))
    im = ax.imshow(pivot.values, aspect="auto", cmap="Blues", vmin=0, vmax=5)
    ax.set_xticks(range(len(LIFECYCLE_STAGES)))
    ax.set_xticklabels(LIFECYCLE_STAGES, fontname="DejaVu Sans")
    ax.set_yticks(range(len(subsectors)))
    ax.set_yticklabels(subsectors, fontname="DejaVu Sans")

    for row_i in range(len(subsectors)):
        for col_i in range(len(LIFECYCLE_STAGES)):
            val = pivot.values[row_i, col_i]
            ax.text(col_i, row_i, f"{val:.1f}", ha="center", va="center",
                    fontsize=9, color="black" if val < 3 else "white", fontname="DejaVu Sans")

    plt.colorbar(im, ax=ax, label="Capability Fit Score (0–5)")
    ax.set_title("Bank Opportunity Heatmap — Top Sectors × Lifecycle Stage",
                 fontname="DejaVu Sans", fontweight="bold")
    plt.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)
```

- [ ] **Step 5: Run figure tests — expect pass**

```bash
pytest tests/test_commercial_layer.py -k "plot_" -v
```
Expected: all 4 tests PASS.

- [ ] **Step 6: Commit**

```bash
git add src/figures.py tests/test_commercial_layer.py
git commit -m "feat: append 4 commercial layer figure functions to figures.py"
```

---

## Task 8: `src/commercial_report.py`

**Files:**
- Create: `src/commercial_report.py`
- Modify: `tests/test_commercial_layer.py`

- [ ] **Step 1: Add failing test**

Append to `tests/test_commercial_layer.py`:

```python
from src.commercial_report import build_commercial_report


def test_commercial_report_generates_file(tmp_path):
    from src.deal_economics import build_deal_economics_summary
    from src.sector_priority import build_sector_priority_ranking
    from src.lifecycle import export_lifecycle_matrix
    from src.bank_strategy import build_bank_strategy_output

    raw_df, summary_df = build_deal_economics_summary(str(tmp_path / "summary.csv"))
    priority = build_sector_priority_ranking(str(tmp_path / "priority.csv"))
    lifecycle = export_lifecycle_matrix(str(tmp_path / "lifecycle.csv"))
    plays, mix, targeting = build_bank_strategy_output(
        plays_path=str(tmp_path / "plays.csv"),
        mix_path=str(tmp_path / "mix.csv"),
        targeting_path=str(tmp_path / "targeting.csv"),
    )
    out = str(tmp_path / "report.md")
    build_commercial_report(priority, raw_df, summary_df, lifecycle, plays, mix, targeting, output_path=out)

    assert os.path.exists(out)
    content = open(out).read()
    assert len(content) > 500
    assert "Where the Money Is" in content
    # All four figure references must appear with correct relative paths
    for fig in [
        "../figures/capital_allocation_by_sector.png",
        "../figures/product_dominance_by_sector.png",
        "../figures/lifecycle_financing_flow.png",
        "../figures/bank_opportunity_heatmap.png",
    ]:
        assert fig in content, f"Missing figure reference: {fig}"
```

- [ ] **Step 2: Run — expect fail**

```bash
pytest tests/test_commercial_layer.py::test_commercial_report_generates_file -v 2>&1 | head -10
```

- [ ] **Step 3: Implement `src/commercial_report.py`**

```python
"""Generate the 'India Sustainable Finance: Where the Money Is' strategy report."""
from __future__ import annotations

import textwrap
from pathlib import Path

import pandas as pd

from src.constants import LIFECYCLE_STAGES, REPORTS_DIR


def _fmt_table(df: pd.DataFrame) -> str:
    """Render a DataFrame as a markdown table string."""
    cols = df.columns.tolist()
    header = "| " + " | ".join(str(c) for c in cols) + " |"
    sep    = "| " + " | ".join("---" for _ in cols) + " |"
    rows   = [
        "| " + " | ".join(str(v) for v in row) + " |"
        for _, row in df.iterrows()
    ]
    return "\n".join([header, sep] + rows)


def build_commercial_report(
    priority_df: pd.DataFrame,
    raw_deal_df: pd.DataFrame,
    summary_deal_df: pd.DataFrame,
    lifecycle_df: pd.DataFrame,
    plays_df: pd.DataFrame,
    mix_df: pd.DataFrame,
    targeting_df: pd.DataFrame,
    output_path: str = f"{REPORTS_DIR}/india_where_the_money_is.md",
) -> None:
    """Generate consulting-style strategy report from commercial layer outputs."""

    total_volume = summary_deal_df["annual_volume_usd_mn"].sum()
    top3_fee = summary_deal_df.nlargest(3, "fee_pool_usd_mn")[["subsector", "fee_pool_usd_mn"]]
    top5 = priority_df[priority_df["top5_flag"]].sort_values("rank")

    lines: list[str] = []

    # ── Title ─────────────────────────────────────────────────────────────
    lines += [
        "# India Sustainable Finance: Where the Money Is",
        "",
        "_Internal strategy reference. All figures are illustrative estimates; not investment advice._",
        "",
        "---",
        "",
    ]

    # ── 1. Executive Summary ───────────────────────────────────────────────
    lines += [
        "## 1. Executive Summary",
        "",
        f"**Total estimated annual financing volume across India's sustainable finance market: "
        f"USD {total_volume:,.0f} mn ({total_volume/1000:.1f} bn).**",
        "",
        "**Three key findings:**",
        "",
    ]
    for i, row in top3_fee.iterrows():
        lines.append(f"{list(top3_fee.index).index(i)+1}. **{row['subsector']}** generates the highest bank fee pool "
                     f"(est. USD {row['fee_pool_usd_mn']:.1f} mn/year).")
    lines += [
        "",
        f"4. Top five priority sectors by composite score: "
        + ", ".join(f"**{r['subsector']}**" for _, r in top5.iterrows()) + ".",
        "",
        "![Capital Allocation by Sector](../figures/capital_allocation_by_sector.png)",
        "",
        "---",
        "",
    ]

    # ── 2. Sector Rankings ─────────────────────────────────────────────────
    lines += [
        "## 2. Sector Rankings",
        "",
        "Subsectors scored 1–5 on four dimensions: total capital required, deal frequency, "
        "bankability, and fee generation potential. Weighted composite score determines priority.",
        "",
    ]
    rank_display = priority_df[["rank", "subsector", "score_capital", "score_frequency",
                                 "score_bankability", "score_fee", "weighted_score", "top5_flag"]].copy()
    rank_display["top5_flag"] = rank_display["top5_flag"].map({True: "★ Top 5", False: ""})
    rank_display.columns = ["Rank", "Subsector", "Capital", "Frequency", "Bankability",
                             "Fee Pool", "Composite", "Priority"]
    lines += [_fmt_table(rank_display), "", "---", ""]

    # ── 3. Deal Archetypes ────────────────────────────────────────────────
    lines += ["## 3. Deal Archetypes — Top 5 Sectors", ""]
    top5_subs = top5["subsector"].tolist()
    for sub in top5_subs:
        row = raw_deal_df[raw_deal_df["subsector"] == sub].iloc[0]
        lines += [
            f"### {sub}",
            "",
            f"- **Archetype:** {row['deal_archetype']}",
            f"- **Typical deal size:** USD {row['deal_size_usd_mn']:.0f} mn",
            f"- **Financing mix:** {row['debt_pct']:.0f}% debt ({row['bond_pct']:.0f}% bonds), "
              f"{row['equity_pct']:.0f}% equity, {row['grant_pct']:.0f}% grants/DFI",
            f"- **Arranger fee:** {row['arranger_fee_bps']:.0f} bps | "
              f"Commitment fee: {row['commitment_fee_bps']:.0f} bps",
            f"- **Sponsor IRR expectation:** {row['irr_expectation_pct']:.0f}%",
            f"- **Estimated deal count (India, annual):** {row['deal_count_annual_estimate']}",
            "",
        ]

    lines += ["---", ""]

    # ── 4. Capital Stack Examples ──────────────────────────────────────────
    lines += [
        "## 4. Capital Stack Examples",
        "",
        "Illustrative capital stacks for the top-5 sector archetypes. "
        "Figures are indicative; actual structures vary by project and market conditions.",
        "",
        "![Capital Allocation by Sector](../figures/capital_allocation_by_sector.png)",
        "",
    ]
    stack_rows = []
    for sub in top5_subs:
        row = raw_deal_df[raw_deal_df["subsector"] == sub].iloc[0]
        dfi = "Yes" if row["grant_pct"] > 0 else "No"
        stack_rows.append({
            "Subsector": sub,
            "Bank Debt %": f"{row['debt_pct'] - row['bond_pct']:.0f}%",
            "Bonds %": f"{row['bond_pct']:.0f}%",
            "Equity %": f"{row['equity_pct']:.0f}%",
            "Blended/DFI %": f"{row['grant_pct']:.0f}%",
            "DFI Involved": dfi,
        })
    lines += [_fmt_table(pd.DataFrame(stack_rows)), "", "---", ""]

    # ── 5. Lifecycle Financing Map ─────────────────────────────────────────
    lines += [
        "## 5. Lifecycle Financing Map",
        "",
        "Optimal financing product at each lifecycle stage, by subsector.",
        "",
        "![Lifecycle Financing Flow](../figures/lifecycle_financing_flow.png)",
        "",
    ]
    lc_display = lifecycle_df[lifecycle_df["subsector"].isin(top5_subs)].copy()
    lc_display = lc_display[["subsector", "stage", "primary_product", "secondary_product", "rationale"]]
    lc_display.columns = ["Subsector", "Stage", "Primary Product", "Secondary Product", "Rationale"]
    lines += [_fmt_table(lc_display), "", "---", ""]

    # ── 6. Bank Strategy Recommendations ──────────────────────────────────
    lines += [
        "## 6. Bank Strategy Recommendations",
        "",
        "Recommendations based on the generic bank capability profile. "
        "Replace `data/bank_capabilities_template.csv` with your institution's profile "
        "and re-run `python build.py --bank-profile <path>` to customise.",
        "",
        "### Top Strategic Plays",
        "",
        "![Bank Opportunity Heatmap](../figures/bank_opportunity_heatmap.png)",
        "",
    ]
    plays_display = plays_df.head(10).copy()
    plays_display.columns = [c.replace("_", " ").title() for c in plays_display.columns]
    lines += [_fmt_table(plays_display), ""]

    lines += ["### Product Mix Recommendation", ""]
    mix_display = mix_df.copy()
    mix_display.columns = [c.replace("_", " ").title() for c in mix_display.columns]
    lines += [_fmt_table(mix_display), ""]

    lines += [
        "![Product Dominance by Sector](../figures/product_dominance_by_sector.png)",
        "",
        "### Client Targeting Strategy",
        "",
    ]
    targeting_display = targeting_df.copy()
    targeting_display.columns = [c.replace("_", " ").title() for c in targeting_display.columns]
    lines += [_fmt_table(targeting_display), "", "---", ""]

    # ── 7. Appendix ────────────────────────────────────────────────────────
    lines += [
        "## 7. Appendix — Methodology and Assumptions",
        "",
        "### Scoring Thresholds",
        "",
        "| Dimension | Score 5 | Score 4 | Score 3 | Score 2 | Score 1 |",
        "|---|---|---|---|---|---|",
        "| Capital Required (USD bn) | ≥50 | ≥20 | ≥10 | ≥5 | <5 |",
        "| Deal Frequency (deals/yr) | ≥20 | ≥10 | ≥5 | ≥2 | <2 |",
        "| Fee Pool (USD mn/yr) | ≥50 | ≥20 | ≥10 | ≥5 | <5 |",
        "| Bankability | Expert judgment (see sector_priority.py BANKABILITY_SCORES) | | | | |",
        "",
        "### Default Weights",
        "",
        "| Dimension | Default Weight |",
        "|---|---|",
        "| Total Capital Required | 30% |",
        "| Deal Frequency | 25% |",
        "| Bankability | 25% |",
        "| Fee Generation | 20% |",
        "",
        "Weights are configurable via `config/priority_weights.yaml`.",
        "",
        "### Data Sources",
        "",
        "- `data/deal_economics.csv` — illustrative deal archetypes; one per subsector",
        "- `data/sector_capital_needs.csv` — illustrative annual capital deployment estimates",
        "- `data/bank_capabilities_template.csv` — generic mid-tier bank capability profile",
        "",
        "All figures are illustrative estimates for strategic analysis purposes. "
        "Not a forecast, not investment advice.",
        "",
    ]

    Path(output_path).write_text("\n".join(lines), encoding="utf-8")
```

- [ ] **Step 4: Run report test — expect pass**

```bash
pytest tests/test_commercial_layer.py::test_commercial_report_generates_file -v
```
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add src/commercial_report.py tests/test_commercial_layer.py
git commit -m "feat: add commercial_report module — Where the Money Is strategy report"
```

---

## Task 9: Wire `build.py`

**Files:**
- Modify: `build.py` (extend `main()`; add `build_commercial_layer()`; add argparse)

> **Important:** `build.py` uses absolute `Path` objects (`ROOT / "reports"`). The new commercial layer modules use relative string paths. Both work correctly when running from the repo root, which is the only supported invocation mode.

- [ ] **Step 1: Read the current end of `build.py` to find the exact insertion point**

```bash
grep -n "if __name__\|def main" build.py
```

- [ ] **Step 2: Add argparse import and `build_commercial_layer()` function**

At the top of `build.py`, add to the import block:
```python
import argparse
from src.constants import DEFAULT_BANK_PROFILE_CSV
```

After the existing `main()` function (before `if __name__ == "__main__":`), add:

```python
def build_commercial_layer(bank_profile_path: str = DEFAULT_BANK_PROFILE_CSV) -> None:
    """Commercial decision-making layer — runs after core research outputs."""
    import os
    os.makedirs("reports", exist_ok=True)
    os.makedirs("figures", exist_ok=True)

    from src.deal_economics import build_deal_economics_summary, compute_annual_financing_volume
    from src.sector_priority import build_sector_priority_ranking, get_top_n
    from src.lifecycle import export_lifecycle_matrix
    from src.bank_strategy import build_bank_strategy_output, load_bank_profile, map_capabilities_to_sectors
    from src.figures import (
        plot_capital_allocation_by_sector,
        plot_product_dominance_by_sector,
        plot_lifecycle_heatmap,
        plot_bank_opportunity_heatmap,
    )
    from src.commercial_report import build_commercial_report

    print("Building commercial layer...")
    raw_df, summary_df = build_deal_economics_summary()
    vol_df    = compute_annual_financing_volume(raw_df)
    priority  = build_sector_priority_ranking()
    lifecycle = export_lifecycle_matrix()

    plays, mix, targeting = build_bank_strategy_output(
        bank_profile_path=bank_profile_path,
        priority_df=priority,
        lifecycle_df=lifecycle,
    )

    plot_capital_allocation_by_sector(vol_df, raw_df)
    plot_product_dominance_by_sector(lifecycle, raw_df)
    plot_lifecycle_heatmap(lifecycle)

    top5 = get_top_n(priority, 5)
    capabilities = load_bank_profile(bank_profile_path)
    mapped = map_capabilities_to_sectors(capabilities, top5, lifecycle)
    plot_bank_opportunity_heatmap(mapped)

    build_commercial_report(priority, raw_df, summary_df, lifecycle, plays, mix, targeting)
    print("Commercial layer complete.")
```

- [ ] **Step 3: Extend `main()` to accept argparse and call `build_commercial_layer()`**

> **Design note:** `build_commercial_layer()` is called from the `__main__` block rather than from inside `main()`. This keeps the existing `main()` function unchanged (zero regression risk). The tradeoff is that programmatic callers of `main()` will not automatically run the commercial layer — they must call `build_commercial_layer()` explicitly. This is the correct tradeoff given the constraint that existing outputs must not be broken.

Replace the `if __name__ == "__main__":` block at the bottom of `build.py`:

```python
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Rebuild all outputs including commercial layer.")
    parser.add_argument(
        "--bank-profile",
        default=DEFAULT_BANK_PROFILE_CSV,
        dest="bank_profile",
        help="Path to bank capabilities CSV (default: data/bank_capabilities_template.csv)",
    )
    args = parser.parse_args()
    main()
    build_commercial_layer(bank_profile_path=args.bank_profile)
```

- [ ] **Step 4: Run the full build and verify no errors**

```bash
python build.py 2>&1
```
Expected: existing outputs regenerated, then "Building commercial layer...", "Commercial layer complete." No errors.

- [ ] **Step 5: Verify all new outputs exist**

```bash
python -c "
import os
expected = [
    'reports/deal_economics_summary.csv',
    'reports/sector_priority_ranking.csv',
    'reports/lifecycle_financing_matrix.csv',
    'reports/bank_strategy_plays.csv',
    'reports/bank_strategy_product_mix.csv',
    'reports/bank_strategy_targeting.csv',
    'reports/india_where_the_money_is.md',
    'figures/capital_allocation_by_sector.png',
    'figures/product_dominance_by_sector.png',
    'figures/lifecycle_financing_flow.png',
    'figures/bank_opportunity_heatmap.png',
]
for p in expected:
    status = '✓' if os.path.exists(p) else '✗ MISSING'
    print(f'{status} {p}')
"
```

- [ ] **Step 6: Verify existing outputs untouched**

```bash
python -c "
import os
existing = [
    'figures/bank_opportunity_matrix.png',
    'figures/capital_channel_split.png',
    'figures/product_recommendation_heatmap.png',
    'figures/subsector_financing_allocation.png',
    'reports/india_transition_financing_roadmap.md',
    'reports/product_mapping_playbook.md',
    'reports/bank_views_SC_DB_UBS.md',
]
for p in existing:
    status = '✓ preserved' if os.path.exists(p) else '✗ MISSING — REGRESSION'
    print(f'{status} {p}')
"
```
Expected: all marked `✓ preserved`.

- [ ] **Step 7: Run full test suite**

```bash
pytest tests/ -v
```
Expected: all tests pass.

- [ ] **Step 8: Commit**

```bash
git add build.py
git commit -m "feat: wire build_commercial_layer into build.py with argparse bank-profile override"
```

---

## Task 10: Push to GitHub

- [ ] **Step 1: Final full test run**

```bash
pytest tests/ -v
```
Expected: all pass.

- [ ] **Step 2: Check git log to confirm all commits are in order**

```bash
git log --oneline -15
```

- [ ] **Step 3: Push to GitHub**

```bash
git push origin main
```

---

## Summary of All New Files

| File | Description |
|---|---|
| `requirements.txt` | +`pyyaml>=6.0` |
| `config/priority_weights.yaml` | Tunable sector scoring weights |
| `data/deal_economics.csv` | 9 deal archetypes with economics |
| `data/sector_capital_needs.csv` | Capital need estimates by subsector |
| `data/bank_capabilities_template.csv` | Generic bank profile template |
| `src/constants.py` | All canonical strings and path constants |
| `src/deal_economics.py` | Volume + fee pool computation |
| `src/sector_priority.py` | Sector scoring and ranking |
| `src/lifecycle.py` | Stage × product matrix |
| `src/bank_strategy.py` | Capability mapping and strategic plays |
| `src/commercial_report.py` | Strategy report generation |
| `src/figures.py` | +4 new figure functions (appended) |
| `build.py` | +`build_commercial_layer()` + argparse |
| `tests/test_commercial_layer.py` | 19 tests for all new modules |
