"""Rebuild all reports, figures, and tabular outputs from source data."""

from __future__ import annotations

from pathlib import Path

from src.bank_views import (
    build_bank_focus_matrix,
    build_bank_plays,
    build_bank_positioning,
    build_opportunity_matrix_numeric,
    build_source_confidence_register,
)
from src.figures import (
    ensure_figure_dir,
    save_bank_opportunity_matrix,
    save_capital_channel_split_chart,
    save_product_recommendation_heatmap,
    save_subsector_allocation_chart,
)
from src.reporting import (
    load_sources,
    render_bank_views_note,
    render_india_transition_roadmap,
    render_product_mapping_playbook,
    render_strategy_appendix,
    write_text_report,
)
from src.scenarios import (
    add_investment_scenarios,
    build_assumption_register,
    build_capital_channel_view,
    build_funding_mix_table,
    build_phase_roadmap,
    build_sector_priority_matrix,
    load_transition_needs,
)
from src.taxonomy import (
    build_borrower_archetype_summary,
    build_corporate_recommendations,
    build_score_matrix,
    build_subsector_recommendations,
    export_product_mapping_table,
    load_corporate_profiles,
    load_product_taxonomy,
)


ROOT = Path(__file__).resolve().parent
REPORTS_DIR = ROOT / "reports"
FIGURES_DIR = ROOT / "figures"
DATA_DIR = ROOT / "data"


def main() -> None:
    """Build all portfolio outputs."""

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    ensure_figure_dir(FIGURES_DIR)

    sources = load_sources(DATA_DIR / "bank_source_ledger.csv")
    transition_needs = load_transition_needs(DATA_DIR / "india_transition_needs.csv")
    scenario_view = add_investment_scenarios(transition_needs)
    funding_mix = build_funding_mix_table()
    capital_channels = build_capital_channel_view(scenario_view)
    phase_roadmap = build_phase_roadmap()
    sector_priority_matrix = build_sector_priority_matrix(scenario_view)
    assumption_register = build_assumption_register()

    products = load_product_taxonomy(DATA_DIR / "product_taxonomy.csv")
    profiles = load_corporate_profiles(DATA_DIR / "example_corporate_profiles.csv")
    product_table = export_product_mapping_table(products)
    subsector_map = build_subsector_recommendations(transition_needs, products, top_n=3)
    corporate_map = build_corporate_recommendations(profiles, transition_needs, products, top_n=3)
    borrower_summary = build_borrower_archetype_summary(
        profiles,
        transition_needs,
        products,
        top_n=2,
    )
    score_matrix = build_score_matrix(transition_needs, products)

    bank_positioning = build_bank_positioning()
    bank_focus_matrix = build_bank_focus_matrix()
    bank_plays = build_bank_plays()
    bank_opportunity_numeric = build_opportunity_matrix_numeric(bank_focus_matrix)
    source_confidence_register = build_source_confidence_register(sources)

    save_subsector_allocation_chart(
        scenario_view,
        FIGURES_DIR / "subsector_financing_allocation.png",
    )
    save_capital_channel_split_chart(
        capital_channels,
        FIGURES_DIR / "capital_channel_split.png",
    )
    save_product_recommendation_heatmap(
        score_matrix,
        FIGURES_DIR / "product_recommendation_heatmap.png",
    )
    save_bank_opportunity_matrix(
        bank_opportunity_numeric,
        FIGURES_DIR / "bank_opportunity_matrix.png",
    )

    write_text_report(
        render_india_transition_roadmap(
            scenario_view,
            funding_mix,
            capital_channels,
            phase_roadmap,
            sources,
            figure_paths={
                "subsector_allocation": "../figures/subsector_financing_allocation.png",
                "capital_channel_split": "../figures/capital_channel_split.png",
            },
        ),
        REPORTS_DIR / "india_transition_financing_roadmap.md",
    )
    write_text_report(
        render_product_mapping_playbook(
            product_table,
            subsector_map,
            corporate_map,
            sources,
            figure_paths={
                "product_heatmap": "../figures/product_recommendation_heatmap.png",
            },
        ),
        REPORTS_DIR / "product_mapping_playbook.md",
    )
    write_text_report(
        render_bank_views_note(
            bank_positioning,
            bank_focus_matrix,
            bank_plays,
            sources,
            figure_paths={"bank_matrix": "../figures/bank_opportunity_matrix.png"},
        ),
        REPORTS_DIR / "bank_views_SC_DB_UBS.md",
    )
    write_text_report(
        render_strategy_appendix(
            bank_positioning,
            sector_priority_matrix,
            borrower_summary,
            source_confidence_register,
            assumption_register,
            sources,
        ),
        REPORTS_DIR / "strategy_appendix.md",
    )

    product_table.to_csv(REPORTS_DIR / "product_mapping_table.csv", index=False)
    bank_positioning.to_csv(REPORTS_DIR / "bank_comparison_matrix.csv", index=False)
    sector_priority_matrix.to_csv(REPORTS_DIR / "india_sector_priority_matrix.csv", index=False)
    borrower_summary.to_csv(REPORTS_DIR / "borrower_archetypes.csv", index=False)
    source_confidence_register.to_csv(REPORTS_DIR / "source_confidence_register.csv", index=False)
    assumption_register.to_csv(REPORTS_DIR / "assumption_register.csv", index=False)

    print("Rebuilt reports, figures, and appendix tables.")


if __name__ == "__main__":
    main()
