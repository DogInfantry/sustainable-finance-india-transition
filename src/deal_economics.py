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
    vol = compute_annual_financing_volume(df)
    fee_cols = df[["subsector", "arranger_fee_bps", "commitment_fee_bps"]].copy()
    result = vol.merge(fee_cols, on="subsector")
    result["weighted_fee_bps"] = (result["arranger_fee_bps"] + result["commitment_fee_bps"]) / 2
    result["fee_pool_usd_mn"] = result["annual_volume_usd_mn"] * result["weighted_fee_bps"] / 10_000
    return (
        result[["subsector", "annual_volume_usd_mn", "weighted_fee_bps", "fee_pool_usd_mn"]]
        .sort_values("fee_pool_usd_mn", ascending=False)
        .reset_index(drop=True)
    )


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
