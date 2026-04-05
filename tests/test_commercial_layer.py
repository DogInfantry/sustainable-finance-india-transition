"""Tests for the commercial decision-making layer."""
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


from src.deal_economics import (
    load_deal_economics,
    compute_annual_financing_volume,
    compute_fee_pool,
    build_deal_economics_summary,
)


def _make_deal_df(n=1):
    """Minimal valid deal DataFrame for testing."""
    from src.constants import SUBSECTORS
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
