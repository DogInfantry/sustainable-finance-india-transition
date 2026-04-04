"""Markdown reporting helpers for the India sustainable finance work sample."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable, Sequence

import pandas as pd


DATA_DIR = Path(__file__).resolve().parents[1] / "data"
REPORTS_DIR = Path(__file__).resolve().parents[1] / "reports"
SOURCE_LEDGER_PATH = DATA_DIR / "bank_source_ledger.csv"


def load_sources(path: Path | str = SOURCE_LEDGER_PATH) -> pd.DataFrame:
    """Load the source ledger."""

    return pd.read_csv(path)


def markdown_table(df: pd.DataFrame, columns: Sequence[str] | None = None) -> str:
    """Render a compact markdown table without external dependencies."""

    view = df.loc[:, columns] if columns else df
    headers = list(view.columns)
    rows = [headers, ["---"] * len(headers)]
    for row in view.itertuples(index=False, name=None):
        rows.append([_escape_cell(value) for value in row])
    return "\n".join("| " + " | ".join(map(str, row)) + " |" for row in rows)


def _escape_cell(value: object) -> str:
    text = "" if pd.isna(value) else str(value)
    return text.replace("\n", "<br>").replace("|", "\\|")


def format_source_list(
    source_ids: Iterable[str], source_ledger: pd.DataFrame | None = None
) -> str:
    """Format a de-duplicated source list for the provided source ids."""

    ledger = load_sources() if source_ledger is None else source_ledger
    selected = ledger[ledger["source_id"].isin(list(dict.fromkeys(source_ids)))]
    lines = []
    for row in selected.itertuples(index=False):
        date_part = (
            f" ({row.publication_date})"
            if isinstance(row.publication_date, str)
            and row.publication_date.strip()
            and row.publication_date != "not verified"
            else ""
        )
        lines.append(
            f"- **{row.source_id}** {row.publication_title}{date_part} - "
            f"[link]({row.url})"
        )
    return "\n".join(lines)


def write_text_report(content: str, output_path: Path | str) -> Path:
    """Write a markdown report to disk."""

    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path


def render_india_transition_roadmap(
    subsector_view: pd.DataFrame,
    funding_mix_view: pd.DataFrame,
    capital_channel_view: pd.DataFrame,
    phase_roadmap: pd.DataFrame,
    source_ledger: pd.DataFrame | None = None,
) -> str:
    """Render the India transition roadmap memo."""

    sources = load_sources() if source_ledger is None else source_ledger
    narrative = """
# India Clean Energy / ESG Financing Roadmap

## Executive Summary

- India's transition financing need is large enough that banks cannot rely on one product family. A practical market build-out needs project finance for contracted assets, green bonds for refinancing and scale, and sustainability-linked structures for diversified corporates and hard-to-abate sectors. [SC3][DB3][DB4]
- The cleanest near-term opportunity set is operating renewables, grid-linked capex, green buildings and distributed-energy portfolios where use-of-proceeds debt can be tied to clearly eligible assets. [SC2][SC5][DB5]
- Industrial decarbonisation, EV ecosystems and fragmented supply chains need more flexible structures: SLLs, transition finance and ESG-linked working-capital lines should be treated as core products, not side products. [SC2][SC4][DB2]

## India Transition Context

Standard Chartered's February 2026 India transition survey says Indian corporates increasingly view green and sustainability-linked loans and bonds as the most relevant instruments, with carbon-market interest rising as the market matures. [SC3] Deutsche Bank's India transition coverage frames the same market through rising power demand, renewable build-out and the need for parallel investment in grid resilience and storage. [DB3][DB6]

For this repository, the country-level annual financing stack is anchored to a **directional** public signal that India's transition could require roughly USD 300 billion per year over time, then split across subsectors using clearly labeled illustrative assumptions. Those subsector allocations are scenario inputs for product mapping, not verified market forecasts. [SC3]

## Illustrative Annual Investment Stack
""".strip()

    subsector_table = markdown_table(
        subsector_view,
        columns=[
            "subsector",
            "central_case_annual_investment_usd_bn",
            "share_of_total_pct",
            "capex_intensity",
            "risk_profile",
            "roadmap_commentary",
        ],
    )
    funding_mix_table = markdown_table(funding_mix_view)
    capital_channel_table = markdown_table(capital_channel_view)
    phase_table = markdown_table(phase_roadmap)

    product_section = """
## Product Logic

- **Project finance beats bond financing** when assets are still under construction, cash flows can be ring-fenced in an SPV, and lenders need tighter covenant control over completion, reserve accounts and step-in rights. Deutsche Bank's project-finance guidance explicitly frames the structure as cash-flow-based and suited to capital-intensive infrastructure. [DB4]
- **Green bonds beat project loans** once issuers have operating assets, repeat issuance needs and a reporting setup that can support portfolio refinancing at scale. Standard Chartered's public sustainable finance messaging and Deutsche Bank's India renewables financing coverage both point to bonds as part of the refinancing and scale-up toolkit. [SC6][DB5]
- **SLLs fit better than green loans** when the funding need is general corporate purpose, the capex plan is broad rather than ring-fenced, or the borrower is in a hard-to-abate sector where transition KPIs matter more than strict green taxonomy eligibility. [SC2][DB2][UBS5]
- **ESG-linked working capital** is the better fit for EPCs, suppliers and mobility ecosystems where the balance-sheet need is short dated and tied to procurement cycles or receivables rather than long-life assets. [SC4][DB5]

## Funding Mix Archetypes
""".strip()

    closing = f"""
## Capital-Pool View

{capital_channel_table}

## Roadmap by Phase

{phase_table}

## Notes and Disclaimers

- All subsector investment figures in this report are **illustrative scenario allocations** used to test product fit. They are not market-size claims and should not be cited as forecasts.
- Verified facts in the narrative above are limited to official public materials from Standard Chartered, Deutsche Bank and UBS. Where bank-specific public evidence was not found, the repository labels the point as not verified rather than filling the gap with inference.
- This repository is an educational work sample and not investment advice.

## Sources

{format_source_list(['SC2', 'SC3', 'SC4', 'SC5', 'SC6', 'DB2', 'DB3', 'DB4', 'DB5', 'DB6', 'UBS5'], sources)}
""".strip()

    return (
        f"{narrative}\n\n{subsector_table}\n\n{product_section}\n\n{funding_mix_table}\n\n{closing}\n"
    )


def render_product_mapping_playbook(
    product_table: pd.DataFrame,
    subsector_recommendations: pd.DataFrame,
    corporate_recommendations: pd.DataFrame,
    source_ledger: pd.DataFrame | None = None,
) -> str:
    """Render the product mapping memo."""

    sources = load_sources() if source_ledger is None else source_ledger
    use_of_proceeds = product_table.loc[
        product_table["Product Family"] == "use of proceeds"
    ]
    linked_and_transition = product_table.loc[
        product_table["Product Family"] != "use of proceeds"
    ]

    sections = [
        "# Product Mapping Playbook",
        "",
        "## Product Taxonomy Overview",
        "",
        "The product set is split deliberately between **use-of-proceeds** instruments and **sustainability-linked or transition** instruments. That matters in India: use-of-proceeds debt is strongest where asset eligibility is clear, while SLLs and transition facilities are more effective when the borrower needs balance-sheet flexibility or is decarbonising hard-to-abate operations. [SC1][SC2][DB2][UBS5]",
        "",
        "### Use-of-Proceeds Products",
        "",
        markdown_table(use_of_proceeds),
        "",
        "### Sustainability-Linked and Transition Products",
        "",
        markdown_table(linked_and_transition),
        "",
        "## Subsector to Product Mapping",
        "",
    ]

    for subsector, frame in subsector_recommendations.groupby("subsector", sort=False):
        sections.extend(
            [
                f"### {subsector}",
                "",
                markdown_table(
                    frame[
                        [
                            "product_name",
                            "product_family",
                            "instrument_type",
                            "score",
                            "why_it_fits",
                        ]
                    ].rename(
                        columns={
                            "product_name": "Product",
                            "product_family": "Family",
                            "instrument_type": "Type",
                            "score": "Score",
                            "why_it_fits": "Rationale",
                        }
                    )
                ),
                "",
            ]
        )

    sections.extend(
        [
            "## Corporate Use-Case Mini Case Studies",
            "",
            "The fictional borrower set below is intentionally realistic but invented. It is designed to show how the same bank toolkit changes when borrower type, credit profile and transition stage change.",
            "",
        ]
    )

    for name, frame in corporate_recommendations.groupby("name", sort=False):
        sections.extend(
            [
                f"### {name}",
                "",
                markdown_table(
                    frame[
                        [
                            "product_name",
                            "product_family",
                            "score",
                            "why_it_fits",
                        ]
                    ].rename(
                        columns={
                            "product_name": "Recommended product",
                            "product_family": "Family",
                            "score": "Score",
                            "why_it_fits": "Why it fits",
                        }
                    )
                ),
                "",
            ]
        )

    sections.extend(
        [
            "## Notes",
            "",
            "- Product scoring is rule-based and explainable. It is intentionally transparent rather than optimized as a black-box model.",
            "- Green securitisation and carbon finance are retained because they are real market instruments, but bank-specific public India evidence for all three banks was not verified in every case. They should be treated as optional scaling tools, not default lead products.",
            "",
            "## Sources",
            "",
            format_source_list(["SC1", "SC2", "SC4", "DB1", "DB2", "DB5", "UBS2", "UBS4", "UBS5"], sources),
        ]
    )

    return "\n".join(sections) + "\n"
