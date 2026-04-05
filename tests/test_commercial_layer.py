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
