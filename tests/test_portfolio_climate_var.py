"""Tests for portfolio_climate_var.py"""
import pytest
import pandas as pd
from src.portfolio_climate_var import PortfolioClimateStress, VALID_SCENARIOS


SAMPLE_HOLDINGS = {
    "Energy": 0.18,
    "Materials": 0.12,
    "Financials": 0.25,
    "IT": 0.20,
    "Consumer": 0.15,
    "Industrials": 0.10,
}


def test_stress_test_returns_dataframe():
    stress = PortfolioClimateStress(SAMPLE_HOLDINGS)
    result = stress.stress_test("transition_2030")
    assert isinstance(result, pd.DataFrame)
    assert "PORTFOLIO TOTAL" in result["sector"].values


def test_portfolio_total_is_negative():
    """Portfolio-level climate VaR should be negative (drawdown)."""
    stress = PortfolioClimateStress(SAMPLE_HOLDINGS)
    result = stress.stress_test("transition_2030")
    total = result[result["sector"] == "PORTFOLIO TOTAL"]["weighted_portfolio_impact_pct"].iloc[0]
    assert total < 0


def test_all_scenarios_run():
    stress = PortfolioClimateStress(SAMPLE_HOLDINGS)
    result = stress.stress_test_all_scenarios()
    assert set(result["scenario"]) == set(VALID_SCENARIOS)


def test_invalid_scenario_raises():
    stress = PortfolioClimateStress(SAMPLE_HOLDINGS)
    with pytest.raises(ValueError, match="not found"):
        stress.stress_test("nonexistent_scenario")


def test_invalid_sector_raises():
    bad_holdings = {"FakeSector": 1.0}
    with pytest.raises(KeyError):
        PortfolioClimateStress(bad_holdings)


def test_weights_not_summing_to_one_raises():
    bad_holdings = {"Energy": 0.5, "IT": 0.1}
    with pytest.raises(ValueError, match="sum to ~1.0"):
        PortfolioClimateStress(bad_holdings)
