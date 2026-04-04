"""Tests for markdown rendering helpers."""

from __future__ import annotations

import pandas as pd

from src.reporting import format_source_list, markdown_image, markdown_link, markdown_table


def test_markdown_link_and_image_helpers_render_relative_paths() -> None:
    assert markdown_link("Roadmap", "./reports/roadmap.md") == "[Roadmap](./reports/roadmap.md)"
    assert markdown_image("Chart", "./figures/chart.png") == "![Chart](./figures/chart.png)"


def test_markdown_table_escapes_pipes_and_newlines() -> None:
    frame = pd.DataFrame({"col": ["alpha|beta", "line1\nline2"]})
    rendered = markdown_table(frame)
    assert "\\|" in rendered
    assert "<br>" in rendered


def test_format_source_list_deduplicates_source_ids() -> None:
    ledger = pd.DataFrame(
        [
            {
                "source_id": "SC1",
                "bank": "Standard Chartered",
                "publication_title": "Example source",
                "publication_date": "2026-01-01",
                "url": "https://example.com",
                "verified_points": "Example",
            }
        ]
    )
    rendered = format_source_list(["SC1", "SC1"], ledger)
    assert rendered.count("**SC1**") == 1
