"""Generate the 'India Sustainable Finance: Where the Money Is' strategy report."""
from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.constants import LIFECYCLE_STAGES, REPORTS_DIR


def _fmt_table(df: pd.DataFrame) -> str:
    """Render a DataFrame as a markdown table string."""
    cols = df.columns.tolist()
    header = "| " + " | ".join(str(c) for c in cols) + " |"
    sep    = "| " + " | ".join("---" for _ in cols) + " |"
    rows   = [
        "| " + " | ".join(str(v) for v in row) + " |"
        for _, row in df.iterrows()
    ]
    return "\n".join([header, sep] + rows)


def build_commercial_report(
    priority_df: pd.DataFrame,
    raw_deal_df: pd.DataFrame,
    summary_deal_df: pd.DataFrame,
    lifecycle_df: pd.DataFrame,
    plays_df: pd.DataFrame,
    mix_df: pd.DataFrame,
    targeting_df: pd.DataFrame,
    output_path: str = f"{REPORTS_DIR}/india_where_the_money_is.md",
) -> None:
    """Generate consulting-style strategy report from commercial layer outputs."""

    total_volume = summary_deal_df["annual_volume_usd_mn"].sum()
    top3_fee = summary_deal_df.nlargest(3, "fee_pool_usd_mn")[["subsector", "fee_pool_usd_mn"]]
    top5 = priority_df[priority_df["top5_flag"]].sort_values("rank")

    lines: list[str] = []

    # ── Title ─────────────────────────────────────────────────────────────
    lines += [
        "# India Sustainable Finance: Where the Money Is",
        "",
        "_Internal strategy reference. All figures are illustrative estimates; not investment advice._",
        "",
        "---",
        "",
    ]

    # ── 1. Executive Summary ───────────────────────────────────────────────
    lines += [
        "## 1. Executive Summary",
        "",
        f"**Total estimated annual financing volume across India's sustainable finance market: "
        f"USD {total_volume:,.0f} mn ({total_volume/1000:.1f} bn).**",
        "",
        "**Three key findings:**",
        "",
    ]
    for i, (_, row) in enumerate(top3_fee.iterrows()):
        lines.append(f"{i+1}. **{row['subsector']}** generates the highest bank fee pool "
                     f"(est. USD {row['fee_pool_usd_mn']:.1f} mn/year).")
    lines += [
        "",
        f"4. Top five priority sectors by composite score: "
        + ", ".join(f"**{r['subsector']}**" for _, r in top5.iterrows()) + ".",
        "",
        "![Capital Allocation by Sector](../figures/capital_allocation_by_sector.png)",
        "",
        "---",
        "",
    ]

    # ── 2. Sector Rankings ─────────────────────────────────────────────────
    lines += [
        "## 2. Sector Rankings",
        "",
        "Subsectors scored 1–5 on four dimensions: total capital required, deal frequency, "
        "bankability, and fee generation potential. Weighted composite score determines priority.",
        "",
    ]
    rank_display = priority_df[["rank", "subsector", "score_capital", "score_frequency",
                                 "score_bankability", "score_fee", "weighted_score", "top5_flag"]].copy()
    rank_display["top5_flag"] = rank_display["top5_flag"].map({True: "★ Top 5", False: ""})
    rank_display.columns = ["Rank", "Subsector", "Capital", "Frequency", "Bankability",
                             "Fee Pool", "Composite", "Priority"]
    lines += [_fmt_table(rank_display), "", "---", ""]

    # ── 3. Deal Archetypes ────────────────────────────────────────────────
    lines += ["## 3. Deal Archetypes — Top 5 Sectors", ""]
    top5_subs = top5["subsector"].tolist()
    for sub in top5_subs:
        row = raw_deal_df[raw_deal_df["subsector"] == sub].iloc[0]
        lines += [
            f"### {sub}",
            "",
            f"- **Archetype:** {row['deal_archetype']}",
            f"- **Typical deal size:** USD {row['deal_size_usd_mn']:.0f} mn",
            f"- **Financing mix:** {row['debt_pct']:.0f}% debt ({row['bond_pct']:.0f}% bonds), "
              f"{row['equity_pct']:.0f}% equity, {row['grant_pct']:.0f}% grants/DFI",
            f"- **Arranger fee:** {row['arranger_fee_bps']:.0f} bps | "
              f"Commitment fee: {row['commitment_fee_bps']:.0f} bps",
            f"- **Sponsor IRR expectation:** {row['irr_expectation_pct']:.0f}%",
            f"- **Estimated deal count (India, annual):** {row['deal_count_annual_estimate']}",
            "",
        ]

    lines += ["---", ""]

    # ── 4. Capital Stack Examples ──────────────────────────────────────────
    lines += [
        "## 4. Capital Stack Examples",
        "",
        "Illustrative capital stacks for the top-5 sector archetypes. "
        "Figures are indicative; actual structures vary by project and market conditions.",
        "",
        "![Capital Allocation by Sector](../figures/capital_allocation_by_sector.png)",
        "",
    ]
    stack_rows = []
    for sub in top5_subs:
        row = raw_deal_df[raw_deal_df["subsector"] == sub].iloc[0]
        dfi = "Yes" if row["grant_pct"] > 0 else "No"
        stack_rows.append({
            "Subsector": sub,
            "Bank Debt %": f"{row['debt_pct'] - row['bond_pct']:.0f}%",
            "Bonds %": f"{row['bond_pct']:.0f}%",
            "Equity %": f"{row['equity_pct']:.0f}%",
            "Blended/DFI %": f"{row['grant_pct']:.0f}%",
            "DFI Involved": dfi,
        })
    lines += [_fmt_table(pd.DataFrame(stack_rows)), "", "---", ""]

    # ── 5. Lifecycle Financing Map ─────────────────────────────────────────
    lines += [
        "## 5. Lifecycle Financing Map",
        "",
        "Optimal financing product at each lifecycle stage, by subsector.",
        "",
        "![Lifecycle Financing Flow](../figures/lifecycle_financing_flow.png)",
        "",
    ]
    lc_display = lifecycle_df[lifecycle_df["subsector"].isin(top5_subs)].copy()
    lc_display = lc_display[["subsector", "stage", "primary_product", "secondary_product", "rationale"]]
    lc_display.columns = ["Subsector", "Stage", "Primary Product", "Secondary Product", "Rationale"]
    lines += [_fmt_table(lc_display), "", "---", ""]

    # ── 6. Bank Strategy Recommendations ──────────────────────────────────
    lines += [
        "## 6. Bank Strategy Recommendations",
        "",
        "Recommendations based on the generic bank capability profile. "
        "Replace `data/bank_capabilities_template.csv` with your institution's profile "
        "and re-run `python build.py --bank-profile <path>` to customise.",
        "",
        "### Top Strategic Plays",
        "",
        "![Bank Opportunity Heatmap](../figures/bank_opportunity_heatmap.png)",
        "",
    ]
    plays_display = plays_df.head(10).copy()
    plays_display.columns = [c.replace("_", " ").title() for c in plays_display.columns]
    lines += [_fmt_table(plays_display), ""]

    lines += ["### Product Mix Recommendation", ""]
    mix_display = mix_df.copy()
    mix_display.columns = [c.replace("_", " ").title() for c in mix_display.columns]
    lines += [_fmt_table(mix_display), ""]

    lines += [
        "![Product Dominance by Sector](../figures/product_dominance_by_sector.png)",
        "",
        "### Client Targeting Strategy",
        "",
    ]
    targeting_display = targeting_df.copy()
    targeting_display.columns = [c.replace("_", " ").title() for c in targeting_display.columns]
    lines += [_fmt_table(targeting_display), "", "---", ""]

    # ── 7. Appendix ────────────────────────────────────────────────────────
    lines += [
        "## 7. Appendix — Methodology and Assumptions",
        "",
        "### Scoring Thresholds",
        "",
        "| Dimension | Score 5 | Score 4 | Score 3 | Score 2 | Score 1 |",
        "|---|---|---|---|---|---|",
        "| Capital Required (USD bn) | ≥50 | ≥20 | ≥10 | ≥5 | <5 |",
        "| Deal Frequency (deals/yr) | ≥20 | ≥10 | ≥5 | ≥2 | <2 |",
        "| Fee Pool (USD mn/yr) | ≥50 | ≥20 | ≥10 | ≥5 | <5 |",
        "| Bankability | Expert judgment (see sector_priority.py BANKABILITY_SCORES) | | | | |",
        "",
        "### Default Weights",
        "",
        "| Dimension | Default Weight |",
        "|---|---|",
        "| Total Capital Required | 30% |",
        "| Deal Frequency | 25% |",
        "| Bankability | 25% |",
        "| Fee Generation | 20% |",
        "",
        "Weights are configurable via `config/priority_weights.yaml`.",
        "",
        "### Data Sources",
        "",
        "- `data/deal_economics.csv` — illustrative deal archetypes; one per subsector",
        "- `data/sector_capital_needs.csv` — illustrative annual capital deployment estimates",
        "- `data/bank_capabilities_template.csv` — generic mid-tier bank capability profile",
        "",
        "All figures are illustrative estimates for strategic analysis purposes. "
        "Not a forecast, not investment advice.",
        "",
    ]

    Path(output_path).write_text("\n".join(lines), encoding="utf-8")
