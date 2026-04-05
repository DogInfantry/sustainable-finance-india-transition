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
