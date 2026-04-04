"""Tests for scenario utilities."""

from __future__ import annotations

import pandas as pd
import pytest

from src.scenarios import (
    SUBSECTOR_ALLOCATION_WEIGHTS,
    add_investment_scenarios,
    build_sector_priority_matrix,
    load_transition_needs,
    validate_subsector_allocations,
)


def test_scenario_allocations_sum_to_100_percent() -> None:
    total = validate_subsector_allocations(SUBSECTOR_ALLOCATION_WEIGHTS)
    assert total == pytest.approx(1.0)

    scenario_view = add_investment_scenarios(load_transition_needs())
    assert scenario_view["share_of_total_pct"].sum() == pytest.approx(100.0)


def test_missing_subsector_validation_raises() -> None:
    subsectors = load_transition_needs()
    extra_row = subsectors.iloc[[0]].copy()
    extra_row.loc[:, "subsector"] = "Green ammonia export hubs"
    invalid = pd.concat([subsectors, extra_row], ignore_index=True)

    with pytest.raises(KeyError):
        add_investment_scenarios(invalid)


def test_sector_priority_matrix_has_priority_labels() -> None:
    matrix = build_sector_priority_matrix(load_transition_needs())
    assert "Priority tier" in matrix.columns
    assert matrix["Priority tier"].str.startswith("Tier").all()
