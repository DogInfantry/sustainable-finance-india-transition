"""Tests for sector_decarbonization_dcf.py"""
import pytest
from src.sector_decarbonization_dcf import SectorDCF, CARBON_PRICE_SCENARIOS


def test_cement_clinker_runs():
    dcf = SectorDCF(sector="cement", technology="clinker_substitution")
    result = dcf.run_valuation(capex_year=2025, carbon_price=5000)
    assert len(result) == 15  # 15-year life
    assert "cumulative_npv_inr_cr" in result.columns


def test_steel_hydrogen_dri_runs():
    dcf = SectorDCF(sector="steel", technology="hydrogen_dri")
    result = dcf.run_valuation(capex_year=2025, carbon_price=5000)
    assert len(result) > 0


def test_coal_plant_retirement():
    dcf = SectorDCF(sector="coal_power", technology="plant_retirement_refinancing")
    result = dcf.run_valuation(capex_year=2025, carbon_price=3000)
    assert len(result) == 20  # retirement horizon


def test_npv_by_carbon_price_returns_all_scenarios():
    dcf = SectorDCF(sector="cement", technology="clinker_substitution")
    result = dcf.npv_by_carbon_price(capex_year=2025)
    assert set(result["scenario"]) == set(CARBON_PRICE_SCENARIOS.keys())


def test_invalid_sector_raises():
    with pytest.raises(ValueError, match="not found"):
        SectorDCF(sector="aviation", technology="saf")


def test_invalid_technology_raises():
    with pytest.raises(ValueError, match="not found"):
        SectorDCF(sector="cement", technology="nuclear")


def test_high_carbon_price_improves_npv():
    dcf = SectorDCF(sector="cement", technology="clinker_substitution")
    low = dcf.npv_by_carbon_price()[dcf.npv_by_carbon_price()["scenario"] == "low"]["terminal_npv_inr_cr"].iloc[0]
    high = dcf.npv_by_carbon_price()[dcf.npv_by_carbon_price()["scenario"] == "high"]["terminal_npv_inr_cr"].iloc[0]
    assert high > low
