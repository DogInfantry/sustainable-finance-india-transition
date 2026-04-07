"""Tests for esg_credit_spread_model.py"""
import pytest
from src.esg_credit_spread_model import ESGSpreadAttributor


def test_attribution_table_has_four_rows():
    attr = ESGSpreadAttributor()
    df = attr.attribution_table()
    assert len(df) == 4


def test_q1_score_no_premium():
    attr = ESGSpreadAttributor()
    spread = attr.estimate_spread(esg_score=80, base_spread_bps=150.0)
    assert spread == 150.0


def test_q4_score_adds_premium():
    attr = ESGSpreadAttributor()
    spread = attr.estimate_spread(esg_score=10, base_spread_bps=150.0)
    assert spread > 150.0


def test_invalid_esg_score_raises():
    attr = ESGSpreadAttributor()
    with pytest.raises(ValueError, match="between 0 and 100"):
        attr.estimate_spread(esg_score=110, base_spread_bps=150.0)


def test_sensitivity_returns_dataframe():
    attr = ESGSpreadAttributor()
    df = attr.score_sensitivity(base_spread_bps=200.0)
    assert len(df) == 21
    assert "total_spread_bps" in df.columns
