"""Rule-based product mapping logic for sustainable finance use cases."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Iterable, Mapping

import pandas as pd


DATA_DIR = Path(__file__).resolve().parents[1] / "data"
PRODUCT_TAXONOMY_PATH = DATA_DIR / "product_taxonomy.csv"
TRANSITION_NEEDS_PATH = DATA_DIR / "india_transition_needs.csv"
CORPORATE_PROFILES_PATH = DATA_DIR / "example_corporate_profiles.csv"

MATURITY_TO_STAGE = {"early": "early", "scaling": "scaling", "mature": "mature"}
SIZE_ORDER = {"small": 1, "mid": 2, "large": 3, "portfolio": 4}
RISK_TO_SHARING = {
    "core": {"on-balance-sheet": 1.8, "distributed": 1.4, "blended": 0.8},
    "core-plus": {"on-balance-sheet": 1.5, "distributed": 1.5, "blended": 1.2},
    "opportunistic": {"on-balance-sheet": 1.0, "distributed": 0.8, "blended": 2.0},
}

DEFAULT_CLIENT_TYPE_BY_SUBSECTOR = {
    "Utility-scale renewables": "developer",
    "Rooftop and behind-the-meter solar": "financial institution",
    "Grid and transmission upgrades": "utility",
    "Battery storage and flexible capacity": "developer",
    "Green buildings and cooling retrofits": "infra fund",
    "EV charging and fleet electrification": "corporate",
    "Industrial decarbonisation": "corporate",
    "Circular economy and resource efficiency": "epc",
}

SUBSECTOR_PRODUCT_BONUS = {
    "Utility-scale renewables": {
        "Green project finance loan": 2.8,
        "Green bond": 1.9,
        "Green corporate term loan": 0.9,
        "Sustainability-linked loan (SLL)": -0.4,
    },
    "Rooftop and behind-the-meter solar": {
        "Green corporate term loan": 1.3,
        "Green securitisation / asset-backed refinancing": 1.8,
        "Blended finance platform (DFI + commercial)": 1.5,
        "Sustainability-linked loan (SLL)": 0.6,
    },
    "Grid and transmission upgrades": {
        "Green project finance loan": 2.5,
        "Green bond": 1.4,
        "Green corporate term loan": 0.8,
        "Sustainability-linked loan (SLL)": -0.8,
    },
    "Battery storage and flexible capacity": {
        "Green project finance loan": 1.5,
        "Blended finance platform (DFI + commercial)": 1.8,
        "Green corporate term loan": 1.0,
        "Sustainability-linked loan (SLL)": 0.4,
    },
    "Green buildings and cooling retrofits": {
        "Green corporate term loan": 1.5,
        "Green bond": 1.2,
        "Sustainability-linked loan (SLL)": 1.2,
    },
    "EV charging and fleet electrification": {
        "Sustainability-linked loan (SLL)": 1.8,
        "ESG-linked working capital / sustainable trade finance": 1.7,
        "Blended finance platform (DFI + commercial)": 1.3,
        "Green securitisation / asset-backed refinancing": 1.1,
    },
    "Industrial decarbonisation": {
        "Transition finance loan": 2.5,
        "Sustainability-linked loan (SLL)": 2.1,
        "Blended finance platform (DFI + commercial)": 1.8,
        "Transition bond": 1.1,
    },
    "Circular economy and resource efficiency": {
        "ESG-linked working capital / sustainable trade finance": 1.6,
        "Sustainability-linked loan (SLL)": 1.4,
        "Carbon finance / results-based finance": 1.2,
        "Blended finance platform (DFI + commercial)": 1.0,
    },
}


def load_product_taxonomy(path: Path | str = PRODUCT_TAXONOMY_PATH) -> pd.DataFrame:
    """Load the product taxonomy reference table."""

    return pd.read_csv(path)


def load_transition_needs(path: Path | str = TRANSITION_NEEDS_PATH) -> pd.DataFrame:
    """Load transition subsectors."""

    return pd.read_csv(path)


def load_corporate_profiles(path: Path | str = CORPORATE_PROFILES_PATH) -> pd.DataFrame:
    """Load the fictional corporate borrower set."""

    return pd.read_csv(path)


def score_product_for_use_case(
    subsector_row: Mapping[str, Any], product_row: Mapping[str, Any]
) -> float:
    """Return a numeric score for the product fit against a subsector or borrower."""

    return round(_evaluate_product_for_use_case(subsector_row, product_row)["score"], 2)


def recommend_products_for_subsector(
    subsector_row: Mapping[str, Any], products: pd.DataFrame, top_n: int = 3
) -> pd.DataFrame:
    """Return the top ranked products for a subsector with explanations."""

    evaluations = [
        _evaluate_product_for_use_case(subsector_row, product)
        for product in products.to_dict(orient="records")
    ]
    ranked = pd.DataFrame(evaluations).sort_values(
        ["score", "product_name"], ascending=[False, True]
    )
    return ranked.head(top_n).reset_index(drop=True)


def recommend_products_for_profile(
    profile_row: Mapping[str, Any],
    subsectors: pd.DataFrame,
    products: pd.DataFrame,
    top_n: int = 3,
) -> pd.DataFrame:
    """Merge borrower and subsector context, then return top product recommendations."""

    matched = subsectors.loc[subsectors["subsector"] == profile_row["subsector"]]
    if matched.empty:
        raise KeyError(f"Unknown subsector for borrower profile: {profile_row['subsector']}")

    merged_context = {
        **matched.iloc[0].to_dict(),
        **dict(profile_row),
        "working_capital_bias": _working_capital_bias(profile_row),
        "bond_market_readiness": _bond_market_readiness(profile_row),
    }
    return recommend_products_for_subsector(merged_context, products, top_n=top_n)


def build_subsector_recommendations(
    subsectors: pd.DataFrame, products: pd.DataFrame, top_n: int = 3
) -> pd.DataFrame:
    """Score all products for all subsectors and keep the top products."""

    frames = []
    for row in subsectors.to_dict(orient="records"):
        ranked = recommend_products_for_subsector(row, products, top_n=top_n)
        ranked.insert(0, "subsector", row["subsector"])
        frames.append(ranked)
    return pd.concat(frames, ignore_index=True)


def build_corporate_recommendations(
    profiles: pd.DataFrame,
    subsectors: pd.DataFrame,
    products: pd.DataFrame,
    top_n: int = 3,
) -> pd.DataFrame:
    """Score products for each fictional borrower profile."""

    frames = []
    for row in profiles.to_dict(orient="records"):
        ranked = recommend_products_for_profile(row, subsectors, products, top_n=top_n)
        ranked.insert(0, "name", row["name"])
        ranked.insert(1, "client_type", row["client_type"])
        ranked.insert(2, "subsector", row["subsector"])
        frames.append(ranked)
    return pd.concat(frames, ignore_index=True)


def export_product_mapping_table(products: pd.DataFrame) -> pd.DataFrame:
    """Create a CSV-ready playbook table with the user's requested columns."""

    return products.rename(
        columns={
            "product_name": "Product",
            "product_family": "Product Family",
            "typical_use_cases": "Best use case",
            "typical_borrower_or_issuer": "Typical borrower / issuer",
            "key_kpis_or_covenants": "Key KPIs or covenants",
            "advantages": "Advantages",
            "risks_limitations": "Risks / limitations",
        }
    )[
        [
            "Product",
            "Product Family",
            "Best use case",
            "Typical borrower / issuer",
            "Key KPIs or covenants",
            "Advantages",
            "Risks / limitations",
        ]
    ]


def _evaluate_product_for_use_case(
    subsector_row: Mapping[str, Any], product_row: Mapping[str, Any]
) -> Dict[str, Any]:
    stage = str(
        subsector_row.get(
            "transition_stage",
            MATURITY_TO_STAGE.get(str(subsector_row.get("market_maturity", "scaling")).lower(), "scaling"),
        )
    ).lower()
    default_client = DEFAULT_CLIENT_TYPE_BY_SUBSECTOR.get(
        str(subsector_row.get("subsector", "")), "corporate"
    )
    client_type = str(subsector_row.get("client_type", default_client)).lower()
    credit_profile = str(subsector_row.get("credit_profile", "not verified")).lower()
    size_bucket = _size_bucket(str(subsector_row.get("typical_project_size_usd", "50-250m")))
    working_capital_bias = (
        float(subsector_row.get("working_capital_bias"))
        if "working_capital_bias" in subsector_row
        else _working_capital_bias(subsector_row)
    )
    bond_market_readiness = (
        float(subsector_row.get("bond_market_readiness"))
        if "bond_market_readiness" in subsector_row
        else _bond_market_readiness(subsector_row)
    )

    score = 0.0
    reasons: list[str] = []

    capex_score = _capex_score(subsector_row, product_row)
    score += capex_score
    if capex_score > 0:
        reasons.append("supports the capex profile")

    size_score = _size_score(size_bucket, product_row)
    score += size_score
    if size_score > 0:
        reasons.append("matches expected ticket size or portfolio scale")

    risk_score = _risk_score(str(subsector_row.get("risk_profile", "core-plus")), product_row)
    score += risk_score
    if risk_score > 0:
        reasons.append("fits the risk-sharing need")

    kpi_score = _kpi_score(str(subsector_row.get("kpi_readiness", "medium")), product_row)
    score += kpi_score
    if kpi_score > 0:
        reasons.append("has KPI mechanics the borrower can likely support")

    taxonomy_score = _taxonomy_score(
        str(subsector_row.get("use_of_proceeds_clarity", "medium")), product_row
    )
    score += taxonomy_score
    if taxonomy_score > 0:
        reasons.append("works with the clarity of eligible use-of-proceeds")

    stage_score = _stage_score(stage, product_row)
    score += stage_score
    if stage_score > 0:
        reasons.append("fits the transition stage")

    if working_capital_bias and _yes_no_value(product_row["appropriate_for_opex"]) > 0:
        wc_score = round(working_capital_bias * 1.8, 2)
        score += wc_score
        reasons.append("captures the borrower's working-capital need")

    if product_row["instrument_type"] == "bond":
        bond_score = bond_market_readiness
        if credit_profile == "investment grade":
            bond_score += 0.8
        elif credit_profile in {"bb", "unrated"}:
            bond_score -= 0.4
        score += bond_score
        if bond_score > 0:
            reasons.append("benefits from bond-market access and refinancing capacity")

    if client_type in {"developer", "utility", "infra fund"} and "project finance" in str(
        product_row["product_name"]
    ).lower():
        score += 1.6
        reasons.append("aligns with asset-level infrastructure financing")

    if client_type in {"corporate", "epc"} and "sustainability-linked loan" in str(
        product_row["product_name"]
    ).lower():
        score += 1.4
        reasons.append("preserves balance-sheet flexibility for diversified corporates")

    if client_type == "financial institution" and product_row["product_name"] in {
        "Green securitisation / asset-backed refinancing",
        "Blended finance platform (DFI + commercial)",
        "Green corporate term loan",
    }:
        score += 1.5
        reasons.append("works for on-lending or portfolio funding models")

    subsector_name = str(subsector_row.get("subsector", "")).lower()
    if "industrial decarbonisation" in subsector_name and str(product_row["hard_to_abate_fit"]).lower() == "high":
        score += 2.2
        reasons.append("is suited to hard-to-abate transition pathways")

    if any(
        segment in subsector_name
        for segment in ["rooftop", "behind-the-meter", "ev charging", "fleet electrification"]
    ) and "securitisation" in str(product_row["product_name"]).lower():
        score += 1.8
        reasons.append("can aggregate fragmented operating assets")

    if "green buildings" in subsector_name and product_row["product_name"] == "Green bond":
        score += 1.0
        reasons.append("matches real-estate portfolio refinancing needs")

    if "grid and transmission" in subsector_name and product_row["product_name"] == "Green project finance loan":
        score += 1.2
        reasons.append("fits long-dated infrastructure construction risk")

    subsector_label = str(subsector_row.get("subsector", ""))
    structured_bonus = SUBSECTOR_PRODUCT_BONUS.get(subsector_label, {}).get(
        str(product_row["product_name"]),
        0.0,
    )
    if structured_bonus:
        score += structured_bonus
        reasons.append("matches the dominant financing pattern for this subsector")

    project_need_bonus = _project_need_bonus(subsector_row, product_row)
    if project_need_bonus:
        score += project_need_bonus
        reasons.append("matches the borrower's current funding objective")

    return {
        "product_name": product_row["product_name"],
        "product_family": product_row["product_family"],
        "instrument_type": product_row["instrument_type"],
        "score": round(score, 2),
        "why_it_fits": "; ".join(dict.fromkeys(reasons)) or "baseline fit only",
        "typical_use_cases": product_row["typical_use_cases"],
        "typical_borrower_or_issuer": product_row["typical_borrower_or_issuer"],
    }


def _capex_score(subsector_row: Mapping[str, Any], product_row: Mapping[str, Any]) -> float:
    capex_intensity = str(subsector_row.get("capex_intensity", "medium")).lower()
    capex_flag = _yes_no_value(product_row["appropriate_for_capex"])
    base = {"high": 2.2, "medium": 1.6, "low": 0.8}.get(capex_intensity, 1.2)
    if capex_flag == 0:
        return -1.4 if capex_intensity in {"high", "medium"} else -0.6
    return round(base * capex_flag, 2)


def _size_score(size_bucket: str, product_row: Mapping[str, Any]) -> float:
    preferred = str(product_row.get("preferred_project_size", "mid")).lower()
    if preferred == size_bucket:
        return 1.8
    if preferred == "portfolio" and size_bucket in {"small", "mid"}:
        return 1.2
    distance = abs(SIZE_ORDER.get(preferred, 2) - SIZE_ORDER.get(size_bucket, 2))
    return 1.0 if distance == 1 else -0.8


def _risk_score(risk_profile: str, product_row: Mapping[str, Any]) -> float:
    sharing = str(product_row.get("risk_sharing", "on-balance-sheet")).lower()
    return RISK_TO_SHARING.get(risk_profile.lower(), RISK_TO_SHARING["core-plus"]).get(
        sharing, 0.6
    )


def _kpi_score(kpi_readiness: str, product_row: Mapping[str, Any]) -> float:
    product_requires_kpi = _yes_no_value(product_row["link_to_KPIs_required"])
    readiness = {"high": 1.8, "medium": 0.9, "low": -0.9}.get(kpi_readiness.lower(), 0.5)
    if product_requires_kpi > 0:
        return readiness
    return 0.5 if kpi_readiness.lower() == "low" else 0.2


def _taxonomy_score(use_of_proceeds_clarity: str, product_row: Mapping[str, Any]) -> float:
    needs_alignment = _yes_no_value(product_row["needs_taxonomy_alignment"])
    clarity_score = {"high": 1.8, "medium": 0.9, "low": -0.8}.get(
        use_of_proceeds_clarity.lower(), 0.5
    )
    if needs_alignment > 0:
        return round(needs_alignment * clarity_score, 2)
    return 0.6 if use_of_proceeds_clarity.lower() == "low" else 0.2


def _stage_score(stage: str, product_row: Mapping[str, Any]) -> float:
    preferred = str(product_row.get("preferred_transition_stage", "scaling")).split("|")
    return 1.3 if stage in {item.strip().lower() for item in preferred} else -0.6


def _size_bucket(raw_value: str) -> str:
    value = raw_value.lower()
    if value.startswith("10-"):
        return "small"
    if value.startswith("50-"):
        return "mid"
    if value.startswith(">"):
        return "large"
    return "mid"


def _yes_no_value(value: Any) -> float:
    text = str(value).strip().lower()
    if text == "yes":
        return 1.0
    if text in {"limited", "depends"}:
        return 0.5
    return 0.0


def _working_capital_bias(row: Mapping[str, Any]) -> float:
    text = str(row.get("key_transition_needs", "")).lower()
    client_type = str(row.get("client_type", "")).lower()
    if client_type in {"epc"}:
        return 1.2
    if any(term in text for term in ["working capital", "receivable", "supplier", "procurement"]):
        return 1.0
    if any(term in text for term in ["warehouse funding", "on-lending"]):
        return 0.8
    return 0.0


def _project_need_bonus(row: Mapping[str, Any], product_row: Mapping[str, Any]) -> float:
    text = str(row.get("key_transition_needs", "")).lower()
    name = str(product_row.get("product_name", "")).lower()
    bonus = 0.0

    if any(term in text for term in ["construction debt", "greenfield", "commission", "smart-meter deployment"]):
        if "project finance" in name:
            bonus += 1.8
        if "green corporate term loan" in name:
            bonus += 0.7

    if any(term in text for term in ["refinancing", "bond market", "take-out", "portfolio refinancing"]):
        if name in {"green bond", "transition bond", "green securitisation / asset-backed refinancing"}:
            bonus += 1.6

    if any(term in text for term in ["working capital", "supplier finance", "receivable", "charger", "battery"]):
        if "working capital" in name or "sustainability-linked loan" in name:
            bonus += 1.4

    return bonus


def _bond_market_readiness(row: Mapping[str, Any]) -> float:
    credit_profile = str(row.get("credit_profile", "")).lower()
    stage = str(row.get("transition_stage", row.get("market_maturity", "scaling"))).lower()
    revenue_scale = str(row.get("revenue_scale", "")).lower()

    score = 0.0
    if credit_profile == "investment grade":
        score += 1.2
    elif credit_profile == "bb":
        score += 0.3
    else:
        score -= 0.6

    if revenue_scale == "large":
        score += 0.8
    elif revenue_scale == "medium":
        score += 0.3

    if stage == "mature":
        score += 0.8
    elif stage == "scaling":
        score += 0.3

    return round(score, 2)
