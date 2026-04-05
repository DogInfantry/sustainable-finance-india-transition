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
