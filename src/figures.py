"""Figure generation utilities for the portfolio-grade repo outputs."""

from __future__ import annotations

from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd


matplotlib.use("Agg")

PRIMARY = "#0B6E4F"
SECONDARY = "#4C956C"
ACCENT = "#2C699A"
LIGHT = "#E9F2EC"
GREY = "#6B7280"


def ensure_figure_dir(path: Path | str) -> Path:
    """Create the figure output directory if needed."""

    figure_dir = Path(path)
    figure_dir.mkdir(parents=True, exist_ok=True)
    return figure_dir


def save_subsector_allocation_chart(
    scenario_view: pd.DataFrame, output_path: Path | str
) -> Path:
    """Save the subsector financing allocation bar chart."""

    fig, ax = plt.subplots(figsize=(11, 6))
    ordered = scenario_view.sort_values("central_case_annual_investment_usd_bn", ascending=True)
    ax.barh(
        ordered["subsector"],
        ordered["central_case_annual_investment_usd_bn"],
        color=PRIMARY,
    )
    ax.set_title("India Transition Financing Allocation by Subsector", loc="left", fontsize=14, weight="bold")
    ax.set_xlabel("Illustrative annual need (USD bn)")
    ax.set_ylabel("")
    ax.grid(axis="x", linestyle="--", alpha=0.3)
    _style_axes(ax)
    return _save_figure(fig, output_path)


def save_capital_channel_split_chart(
    capital_channel_view: pd.DataFrame, output_path: Path | str
) -> Path:
    """Save the capital-channel split stacked bar chart."""

    fig, ax = plt.subplots(figsize=(11, 6))
    ordered = capital_channel_view.set_index("subsector")
    colors = [PRIMARY, ACCENT, SECONDARY, "#D0A85C"]
    ordered.plot(kind="barh", stacked=True, ax=ax, color=colors, width=0.8)
    ax.set_title("Capital-Channel Split by Subsector", loc="left", fontsize=14, weight="bold")
    ax.set_xlabel("Illustrative annual need (USD bn)")
    ax.set_ylabel("")
    ax.legend(
        ["Bank balance sheet", "Public markets", "Blended / DFI", "Carbon-linked"],
        frameon=False,
        loc="lower right",
    )
    ax.grid(axis="x", linestyle="--", alpha=0.3)
    _style_axes(ax)
    return _save_figure(fig, output_path)


def save_product_recommendation_heatmap(
    score_matrix: pd.DataFrame, output_path: Path | str, top_n: int = 12
) -> Path:
    """Save the product recommendation heatmap."""

    ranked = score_matrix.copy()
    ranked["average_score"] = ranked.mean(axis=1)
    ranked = ranked.sort_values("average_score", ascending=False).drop(columns=["average_score"]).head(top_n)

    fig, ax = plt.subplots(figsize=(12, 8))
    image = ax.imshow(ranked.to_numpy(), cmap="YlGnBu", aspect="auto")
    ax.set_title("Product Recommendation Heatmap", loc="left", fontsize=14, weight="bold")
    ax.set_xticks(range(len(ranked.columns)))
    ax.set_xticklabels(ranked.columns, rotation=45, ha="right")
    ax.set_yticks(range(len(ranked.index)))
    ax.set_yticklabels(ranked.index)
    for row in range(ranked.shape[0]):
        for col in range(ranked.shape[1]):
            ax.text(col, row, f"{ranked.iat[row, col]:.1f}", ha="center", va="center", fontsize=8, color="black")
    fig.colorbar(image, ax=ax, shrink=0.8, label="Rule-based score")
    _style_axes(ax)
    return _save_figure(fig, output_path)


def save_bank_opportunity_matrix(
    numeric_matrix: pd.DataFrame, output_path: Path | str
) -> Path:
    """Save the bank opportunity matrix heatmap."""

    fig, ax = plt.subplots(figsize=(11, 5))
    image = ax.imshow(numeric_matrix.to_numpy(), cmap="Greens", aspect="auto", vmin=0, vmax=4)
    ax.set_title("Bank Opportunity Matrix", loc="left", fontsize=14, weight="bold")
    ax.set_xticks(range(len(numeric_matrix.columns)))
    ax.set_xticklabels(numeric_matrix.columns, rotation=35, ha="right")
    ax.set_yticks(range(len(numeric_matrix.index)))
    ax.set_yticklabels(numeric_matrix.index)
    for row in range(numeric_matrix.shape[0]):
        for col in range(numeric_matrix.shape[1]):
            ax.text(col, row, f"{numeric_matrix.iat[row, col]:.1f}", ha="center", va="center", fontsize=8)
    fig.colorbar(image, ax=ax, shrink=0.8, label="Opportunity intensity")
    _style_axes(ax)
    return _save_figure(fig, output_path)


def _style_axes(ax: plt.Axes) -> None:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(LIGHT)
    ax.spines["bottom"].set_color(LIGHT)
    ax.tick_params(colors=GREY)


def _save_figure(fig: plt.Figure, output_path: Path | str) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    return path
