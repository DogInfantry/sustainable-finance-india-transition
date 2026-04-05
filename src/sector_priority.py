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
    """Score each subsector 1-5 on four dimensions and return ranked DataFrame."""
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
