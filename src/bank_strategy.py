"""Bank strategy engine: map bank capabilities to sector opportunities."""
from __future__ import annotations

import pandas as pd

from src.constants import (
    DEFAULT_BANK_PROFILE_CSV,
    DEFAULT_CLIENT_SEGMENT,
    LIFECYCLE_STAGES,
    PRODUCT_CATEGORIES,
    PRODUCT_CATEGORY_MAP,
    REPORTS_DIR,
)


def load_bank_profile(path: str = DEFAULT_BANK_PROFILE_CSV) -> pd.DataFrame:
    """Load bank capabilities CSV. Validates required columns."""
    df = pd.read_csv(path)
    for col in ("capability", "strength", "client_segment", "india_presence"):
        if col not in df.columns:
            raise ValueError(f"Missing required column '{col}' in {path}")
    return df


def _lookup_strength(capabilities_df: pd.DataFrame, product: str) -> float:
    """Case-insensitive match; returns max strength or 0."""
    folded = product.casefold()
    matches = capabilities_df[capabilities_df["capability"].str.casefold() == folded]
    if matches.empty:
        return 0.0
    return float(matches["strength"].max())


def map_capabilities_to_sectors(
    capabilities_df: pd.DataFrame,
    priority_df: pd.DataFrame,
    lifecycle_df: pd.DataFrame,
) -> pd.DataFrame:
    """Cross-map bank capabilities against top-N sectors × lifecycle stages."""
    rows = []
    for _, p_row in priority_df.iterrows():
        sub = p_row["subsector"]
        sub_lc = lifecycle_df[lifecycle_df["subsector"] == sub]
        for _, lc_row in sub_lc.iterrows():
            ps = _lookup_strength(capabilities_df, lc_row["primary_product"])
            ss = _lookup_strength(capabilities_df, lc_row["secondary_product"])
            fit = ps + 0.5 * ss
            fit_norm = round(fit / 7.5 * 5, 2)
            rows.append({
                "subsector":           sub,
                "stage":               lc_row["stage"],
                "primary_product":     lc_row["primary_product"],
                "secondary_product":   lc_row["secondary_product"],
                "primary_strength":    ps,
                "secondary_strength":  ss,
                "fit_score":           fit,
                "fit_score_normalised": fit_norm,
            })
    return pd.DataFrame(rows)


def get_top_strategic_plays(mapped_df: pd.DataFrame) -> pd.DataFrame:
    """Return ranked strategic plays with recommended action."""
    df = mapped_df.copy().sort_values("fit_score_normalised", ascending=False).reset_index(drop=True)
    df["rank"] = range(1, len(df) + 1)

    def _action(score: float) -> str:
        if score >= 4.0:
            return "Lead Arranger"
        if score >= 2.5:
            return "Co-Arranger"
        return "Build Capability / Partner"

    df["recommended_action"] = df["fit_score_normalised"].apply(_action)
    return df[["rank", "subsector", "stage", "recommended_action", "fit_score_normalised"]]


def get_product_mix_recommendation(mapped_df: pd.DataFrame) -> pd.DataFrame:
    """Return % allocation across PRODUCT_CATEGORIES. Equal split if all scores zero."""
    cat_scores: dict[str, float] = {cat: 0.0 for cat in PRODUCT_CATEGORIES}
    for _, row in mapped_df.iterrows():
        cat = PRODUCT_CATEGORY_MAP.get(row["primary_product"])
        if cat:
            cat_scores[cat] += row["fit_score_normalised"]
    total = sum(cat_scores.values())
    rows = []
    for cat, score in cat_scores.items():
        pct = (score / total * 100) if total > 0 else 25.0
        rows.append({"product_category": cat, "total_fit_score": score, "recommended_allocation_pct": round(pct, 2)})
    return pd.DataFrame(rows)


def get_client_targeting_strategy(
    mapped_df: pd.DataFrame,
    capabilities_df: pd.DataFrame,
) -> pd.DataFrame:
    """Return entry point per subsector with client segment and rationale."""
    stage_order = {s: i for i, s in enumerate(LIFECYCLE_STAGES)}
    rows = []
    for sub in mapped_df["subsector"].unique():
        sub_df = mapped_df[mapped_df["subsector"] == sub].copy()
        sub_df["_stage_order"] = sub_df["stage"].map(stage_order)
        best = sub_df.sort_values(
            ["fit_score_normalised", "_stage_order"], ascending=[False, True]
        ).iloc[0]

        product = best["primary_product"]
        folded = product.casefold()
        matches = capabilities_df[capabilities_df["capability"].str.casefold() == folded]
        if matches.empty:
            segment = DEFAULT_CLIENT_SEGMENT
        else:
            segment = matches.sort_values("strength", ascending=False).iloc[0]["client_segment"]

        rows.append({
            "subsector":      sub,
            "client_segment": segment,
            "entry_stage":    best["stage"],
            "entry_point":    product,
            "rationale":      f"Highest capability fit at {best['stage']} stage (score {best['fit_score_normalised']})",
        })
    return pd.DataFrame(rows)


def build_bank_strategy_output(
    bank_profile_path: str = DEFAULT_BANK_PROFILE_CSV,
    priority_df: "pd.DataFrame | None" = None,
    lifecycle_df: "pd.DataFrame | None" = None,
    n_sectors: int = 5,
    plays_path: str = f"{REPORTS_DIR}/bank_strategy_plays.csv",
    mix_path:   str = f"{REPORTS_DIR}/bank_strategy_product_mix.csv",
    targeting_path: str = f"{REPORTS_DIR}/bank_strategy_targeting.csv",
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Orchestrate full bank strategy output. Returns (plays, mix, targeting)."""
    from src.lifecycle import export_lifecycle_matrix
    from src.sector_priority import build_sector_priority_ranking, get_top_n

    capabilities = load_bank_profile(bank_profile_path)
    if priority_df is None:
        priority_df = build_sector_priority_ranking()
    if lifecycle_df is None:
        lifecycle_df = export_lifecycle_matrix()

    top_n = get_top_n(priority_df, n_sectors)
    if len(top_n) == 0:
        raise ValueError("No subsectors to map — check sector_priority output.")

    mapped    = map_capabilities_to_sectors(capabilities, top_n, lifecycle_df)
    plays     = get_top_strategic_plays(mapped)
    mix       = get_product_mix_recommendation(mapped)
    targeting = get_client_targeting_strategy(mapped, capabilities)

    plays.to_csv(plays_path, index=False)
    mix.to_csv(mix_path, index=False)
    targeting.to_csv(targeting_path, index=False)
    return plays, mix, targeting
