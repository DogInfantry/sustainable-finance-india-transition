"""Tests for product scoring logic."""

from __future__ import annotations

from src.taxonomy import (
    load_product_taxonomy,
    load_transition_needs,
    recommend_products_for_subsector,
)


def test_utility_scale_renewables_prefers_project_finance() -> None:
    subsectors = load_transition_needs()
    products = load_product_taxonomy()
    renewables = subsectors.loc[
        subsectors["subsector"] == "Utility-scale renewables"
    ].iloc[0]

    recommendations = recommend_products_for_subsector(renewables, products, top_n=3)
    assert recommendations.iloc[0]["product_name"] == "Green project finance loan"


def test_industrial_decarbonisation_prefers_transition_or_sll_products() -> None:
    subsectors = load_transition_needs()
    products = load_product_taxonomy()
    industry = subsectors.loc[
        subsectors["subsector"] == "Industrial decarbonisation"
    ].iloc[0]

    recommendations = recommend_products_for_subsector(industry, products, top_n=3)
    top_names = set(recommendations["product_name"])
    assert "Transition finance loan" in top_names
    assert "Sustainability-linked loan (SLL)" in top_names
