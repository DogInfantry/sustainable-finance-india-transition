"""Scenario utilities for the India clean energy financing roadmap."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, Mapping

import pandas as pd


DATA_DIR = Path(__file__).resolve().parents[1] / "data"
INDIA_TRANSITION_NEEDS_PATH = DATA_DIR / "india_transition_needs.csv"

# Directional public anchor: Standard Chartered's India transition commentary
# says annual investment needs could reach roughly USD 300bn. Subsector splits
# below are illustrative scenario assumptions rather than sourced forecasts.
PUBLIC_ANCHOR_ANNUAL_NEED_USD_BN = 300.0
LOW_CASE_MULTIPLIER = 0.75
HIGH_CASE_MULTIPLIER = 1.25

SUBSECTOR_ALLOCATION_WEIGHTS: Dict[str, float] = {
    "Utility-scale renewables": 0.27,
    "Rooftop and behind-the-meter solar": 0.08,
    "Grid and transmission upgrades": 0.18,
    "Battery storage and flexible capacity": 0.11,
    "Green buildings and cooling retrofits": 0.08,
    "EV charging and fleet electrification": 0.11,
    "Industrial decarbonisation": 0.13,
    "Circular economy and resource efficiency": 0.04,
}

CAPITAL_CHANNEL_BIASES: Dict[str, Mapping[str, float]] = {
    "Utility-scale renewables": {
        "bank_balance_sheet_pct": 0.35,
        "public_markets_pct": 0.35,
        "blended_dfi_pct": 0.15,
        "carbon_markets_pct": 0.15,
    },
    "Rooftop and behind-the-meter solar": {
        "bank_balance_sheet_pct": 0.40,
        "public_markets_pct": 0.20,
        "blended_dfi_pct": 0.25,
        "carbon_markets_pct": 0.15,
    },
    "Grid and transmission upgrades": {
        "bank_balance_sheet_pct": 0.45,
        "public_markets_pct": 0.35,
        "blended_dfi_pct": 0.15,
        "carbon_markets_pct": 0.05,
    },
    "Battery storage and flexible capacity": {
        "bank_balance_sheet_pct": 0.35,
        "public_markets_pct": 0.20,
        "blended_dfi_pct": 0.30,
        "carbon_markets_pct": 0.15,
    },
    "Green buildings and cooling retrofits": {
        "bank_balance_sheet_pct": 0.35,
        "public_markets_pct": 0.30,
        "blended_dfi_pct": 0.10,
        "carbon_markets_pct": 0.25,
    },
    "EV charging and fleet electrification": {
        "bank_balance_sheet_pct": 0.35,
        "public_markets_pct": 0.20,
        "blended_dfi_pct": 0.25,
        "carbon_markets_pct": 0.20,
    },
    "Industrial decarbonisation": {
        "bank_balance_sheet_pct": 0.35,
        "public_markets_pct": 0.15,
        "blended_dfi_pct": 0.35,
        "carbon_markets_pct": 0.15,
    },
    "Circular economy and resource efficiency": {
        "bank_balance_sheet_pct": 0.35,
        "public_markets_pct": 0.10,
        "blended_dfi_pct": 0.25,
        "carbon_markets_pct": 0.30,
    },
}

SUBSECTOR_PRODUCT_FIT: Dict[str, str] = {
    "Utility-scale renewables": "Project finance is the cleanest lead product for contracted greenfield assets; green bonds become more efficient after commissioning or for portfolio refinancing.",
    "Rooftop and behind-the-meter solar": "Warehouse lines, on-lending facilities and green securitisation are more scalable than single-asset bonds in fragmented distributed portfolios.",
    "Grid and transmission upgrades": "Long-dated project or corporate infrastructure loans work earlier in the build cycle, while bonds are better once regulated or availability-based assets are operating.",
    "Battery storage and flexible capacity": "Use-of-proceeds debt works when contracted revenues are visible; blended structures help where merchant exposure or policy support is still evolving.",
    "Green buildings and cooling retrofits": "Green loans and green bonds suit ring-fenced capex, while SLLs fit diversified real-estate groups with enterprise-wide efficiency KPIs.",
    "EV charging and fleet electrification": "SLLs and ESG-linked working capital fit scaling operators better than standalone bonds; warehouse and blended structures help aggregate small assets.",
    "Industrial decarbonisation": "SLLs and transition finance fit best when the borrower needs balance-sheet flexibility and KPI-linked incentives, not a narrow green capex bucket.",
    "Circular economy and resource efficiency": "Working-capital lines, SLLs and carbon-linked revenue support can unlock smaller-ticket projects that are too fragmented for public bonds.",
}

SECTOR_BANKABILITY_MAP: Dict[tuple[str, str], str] = {
    ("mature", "core"): "High",
    ("mature", "core-plus"): "High",
    ("scaling", "core-plus"): "Medium-High",
    ("scaling", "opportunistic"): "Medium",
    ("early", "opportunistic"): "Catalytic",
    ("early", "core-plus"): "Medium",
}


@dataclass(frozen=True)
class FundingMix:
    """Simple funding archetype for roadmap discussions."""

    archetype: str
    debt_pct: float
    equity_pct: float
    blended_concessional_pct: float
    carbon_and_other_pct: float


FUNDING_MIX_ARCHETYPES: tuple[FundingMix, ...] = (
    FundingMix(
        archetype="Base-case",
        debt_pct=0.62,
        equity_pct=0.25,
        blended_concessional_pct=0.10,
        carbon_and_other_pct=0.03,
    ),
    FundingMix(
        archetype="Accelerated transition",
        debt_pct=0.55,
        equity_pct=0.22,
        blended_concessional_pct=0.18,
        carbon_and_other_pct=0.05,
    ),
)


def load_transition_needs(path: Path | str = INDIA_TRANSITION_NEEDS_PATH) -> pd.DataFrame:
    """Load the transition subsector reference table."""

    return pd.read_csv(path)


def validate_subsector_allocations(
    allocation_weights: Mapping[str, float] | None = None,
) -> float:
    """Validate that scenario allocation weights sum to 100%."""

    weights = dict(SUBSECTOR_ALLOCATION_WEIGHTS if allocation_weights is None else allocation_weights)
    total = round(sum(weights.values()), 6)
    if abs(total - 1.0) > 1e-6:
        raise ValueError(
            f"Subsector allocation weights must sum to 1.0, received {total:.6f}."
        )
    return total


def validate_subsector_inputs(
    subsectors: pd.DataFrame,
    allocation_weights: Mapping[str, float] | None = None,
    capital_channel_biases: Mapping[str, Mapping[str, float]] | None = None,
) -> None:
    """Validate that each subsector has scenario and capital-channel coverage."""

    weights = SUBSECTOR_ALLOCATION_WEIGHTS if allocation_weights is None else allocation_weights
    channels = CAPITAL_CHANNEL_BIASES if capital_channel_biases is None else capital_channel_biases

    missing_weights = set(subsectors["subsector"]) - set(weights)
    if missing_weights:
        raise KeyError(f"Missing allocation weights for subsectors: {sorted(missing_weights)}")

    missing_channels = set(subsectors["subsector"]) - set(channels)
    if missing_channels:
        raise KeyError(
            f"Missing capital-channel biases for subsectors: {sorted(missing_channels)}"
        )

    validate_subsector_allocations(weights)


def add_investment_scenarios(
    subsectors: pd.DataFrame,
    total_annual_need_usd_bn: float = PUBLIC_ANCHOR_ANNUAL_NEED_USD_BN,
    low_multiplier: float = LOW_CASE_MULTIPLIER,
    high_multiplier: float = HIGH_CASE_MULTIPLIER,
) -> pd.DataFrame:
    """Attach low, central and high illustrative annual investment assumptions."""

    validate_subsector_inputs(subsectors)

    df = subsectors.copy()
    df["allocation_weight"] = df["subsector"].map(SUBSECTOR_ALLOCATION_WEIGHTS)
    df["central_case_annual_investment_usd_bn"] = (
        df["allocation_weight"] * total_annual_need_usd_bn
    ).round(1)
    df["low_case_annual_investment_usd_bn"] = (
        df["central_case_annual_investment_usd_bn"] * low_multiplier
    ).round(1)
    df["high_case_annual_investment_usd_bn"] = (
        df["central_case_annual_investment_usd_bn"] * high_multiplier
    ).round(1)
    df["share_of_total_pct"] = (df["allocation_weight"] * 100).round(1)
    df["roadmap_commentary"] = df["subsector"].map(SUBSECTOR_PRODUCT_FIT)
    return df.sort_values(
        "central_case_annual_investment_usd_bn", ascending=False
    ).reset_index(drop=True)


def build_funding_mix_table(
    total_annual_need_usd_bn: float = PUBLIC_ANCHOR_ANNUAL_NEED_USD_BN,
    archetypes: Iterable[FundingMix] = FUNDING_MIX_ARCHETYPES,
) -> pd.DataFrame:
    """Convert funding mix archetypes into a tabular view with implied amounts."""

    rows = []
    for archetype in archetypes:
        rows.append(
            {
                "archetype": archetype.archetype,
                "debt_pct": round(archetype.debt_pct * 100, 1),
                "equity_pct": round(archetype.equity_pct * 100, 1),
                "blended_concessional_pct": round(
                    archetype.blended_concessional_pct * 100, 1
                ),
                "carbon_and_other_pct": round(archetype.carbon_and_other_pct * 100, 1),
                "debt_usd_bn": round(total_annual_need_usd_bn * archetype.debt_pct, 1),
                "equity_usd_bn": round(
                    total_annual_need_usd_bn * archetype.equity_pct, 1
                ),
                "blended_concessional_usd_bn": round(
                    total_annual_need_usd_bn * archetype.blended_concessional_pct, 1
                ),
                "carbon_and_other_usd_bn": round(
                    total_annual_need_usd_bn * archetype.carbon_and_other_pct, 1
                ),
            }
        )

    return pd.DataFrame(rows)


def build_capital_channel_view(subsectors: pd.DataFrame) -> pd.DataFrame:
    """Allocate each subsector's central case across broad capital channels."""

    rows = []
    for record in subsectors.to_dict(orient="records"):
        channel_bias = CAPITAL_CHANNEL_BIASES[record["subsector"]]
        rows.append(
            {
                "subsector": record["subsector"],
                "bank_balance_sheet_usd_bn": round(
                    record["central_case_annual_investment_usd_bn"]
                    * channel_bias["bank_balance_sheet_pct"],
                    1,
                ),
                "public_markets_usd_bn": round(
                    record["central_case_annual_investment_usd_bn"]
                    * channel_bias["public_markets_pct"],
                    1,
                ),
                "blended_dfi_usd_bn": round(
                    record["central_case_annual_investment_usd_bn"]
                    * channel_bias["blended_dfi_pct"],
                    1,
                ),
                "carbon_markets_usd_bn": round(
                    record["central_case_annual_investment_usd_bn"]
                    * channel_bias["carbon_markets_pct"],
                    1,
                ),
            }
        )
    return pd.DataFrame(rows)


def build_phase_roadmap() -> pd.DataFrame:
    """Return an actionable phase-based roadmap."""

    return pd.DataFrame(
        [
            {
                "phase": "0-12 months",
                "priority": "Win refinancing and shovel-ready assets",
                "actions": (
                    "Prioritise operating renewables, smart-metering, certified "
                    "buildings and grid-linked capex where use-of-proceeds debt can "
                    "close quickly. Build SLL pipelines for industrial and mobility "
                    "borrowers that are not yet green-bond ready."
                ),
                "products": (
                    "Green project finance, green corporate loans, green bonds, "
                    "SLLs, ESG-linked working capital."
                ),
            },
            {
                "phase": "12-36 months",
                "priority": "Scale portfolio platforms and transition pathways",
                "actions": (
                    "Aggregate distributed solar, storage, EV and retrofit assets "
                    "into warehouse or securitisation-ready pools. Structure "
                    "transition finance programmes for steel, cement and chemicals "
                    "with milestone-based KPI calibration."
                ),
                "products": (
                    "Green bonds, green securitisation, transition loans, SLBs, "
                    "blended finance platforms."
                ),
            },
            {
                "phase": "3-5 years",
                "priority": "Industrialise capital markets and blended pools",
                "actions": (
                    "Move mature portfolios to repeat issuance, crowd in insurers and "
                    "wealth capital, and use blended or carbon-linked structures for "
                    "harder technologies such as green hydrogen, long-duration storage "
                    "and process decarbonisation."
                ),
                "products": (
                    "Programmatic green bonds, transition bonds, securitisation, "
                    "blended finance, carbon finance."
                ),
            },
        ]
    )


def build_sector_priority_matrix(subsectors: pd.DataFrame) -> pd.DataFrame:
    """Build a consulting-style sector priority matrix for the appendix report."""

    def _priority_tier(row: pd.Series) -> str:
        if row["central_case_annual_investment_usd_bn"] >= 40 and row["bankability"] in {
            "High",
            "Medium-High",
        }:
            return "Tier 1"
        if row["bankability"] == "Catalytic" or row["market_maturity"] == "early":
            return "Tier 2 - catalytic"
        return "Tier 2"

    df = subsectors.copy()
    if "central_case_annual_investment_usd_bn" not in df.columns:
        df = add_investment_scenarios(df)

    df["bankability"] = df.apply(
        lambda row: SECTOR_BANKABILITY_MAP.get(
            (str(row["market_maturity"]).lower(), str(row["risk_profile"]).lower()),
            "Medium",
        ),
        axis=1,
    )
    df["priority_tier"] = df.apply(_priority_tier, axis=1)
    df["commercial_read_through"] = df.apply(
        lambda row: _sector_opportunity_commentary(row["subsector"], row["priority_tier"]),
        axis=1,
    )
    return df[
        [
            "subsector",
            "central_case_annual_investment_usd_bn",
            "market_maturity",
            "capex_intensity",
            "bankability",
            "priority_tier",
            "commercial_read_through",
        ]
    ].rename(
        columns={
            "subsector": "Subsector",
            "central_case_annual_investment_usd_bn": "Illustrative annual need (USD bn)",
            "market_maturity": "Market maturity",
            "capex_intensity": "Capex intensity",
            "bankability": "Bankability",
            "priority_tier": "Priority tier",
            "commercial_read_through": "Commercial read-through",
        }
    )


def build_assumption_register() -> pd.DataFrame:
    """Return the model assumption register used in the portfolio appendix."""

    return pd.DataFrame(
        [
            {
                "Area": "Country financing anchor",
                "Assumption": "USD 300bn annual transition financing need used as the central illustrative anchor.",
                "Treatment": "Illustrative scenario input",
                "Confidence": "Medium",
                "Why it matters": "Sets the order-of-magnitude envelope for subsector allocation and capital-pool sizing.",
            },
            {
                "Area": "Subsector splits",
                "Assumption": "Allocation weights translate the country anchor across eight transition subsectors.",
                "Treatment": "Illustrative scenario input",
                "Confidence": "Medium",
                "Why it matters": "Determines where products are shown to scale first.",
            },
            {
                "Area": "Capital-channel mix",
                "Assumption": "Each subsector is split across bank balance sheet, public markets, blended / DFI, and carbon-linked pools.",
                "Treatment": "Illustrative scenario input",
                "Confidence": "Medium-Low",
                "Why it matters": "Frames where each bank can realistically originate or distribute capital.",
            },
            {
                "Area": "Borrower archetypes",
                "Assumption": "Corporate profiles are fictional but realistic and are not intended to represent actual clients.",
                "Treatment": "Design choice",
                "Confidence": "High",
                "Why it matters": "Allows product-stack demonstration without client confidentiality concerns.",
            },
            {
                "Area": "Product scoring",
                "Assumption": "Rule-based scoring prioritises explainability over statistical optimisation.",
                "Treatment": "Method choice",
                "Confidence": "High",
                "Why it matters": "Keeps the work sample interpretable for strategy and origination discussions.",
            },
        ]
    )


def _sector_opportunity_commentary(subsector: str, tier: str) -> str:
    commentary = {
        "Utility-scale renewables": "Large addressable pool for project finance, syndicated debt and refinancing bonds.",
        "Rooftop and behind-the-meter solar": "Requires warehouse, aggregation and on-lending structures rather than single-asset capital markets.",
        "Grid and transmission upgrades": "Favors long-dated infrastructure debt and later-stage refinancing once regulated cash flows are visible.",
        "Battery storage and flexible capacity": "Commercially attractive but still benefits from catalytic or risk-sharing overlays.",
        "Green buildings and cooling retrofits": "Steady pipeline for green loans, green bonds and real-estate refinancing mandates.",
        "EV charging and fleet electrification": "Needs combined capex and working-capital toolkit, particularly for operators and suppliers.",
        "Industrial decarbonisation": "High strategic value but more transition- and KPI-led than pure green use-of-proceeds.",
        "Circular economy and resource efficiency": "Smaller ticket sizes favor structured working capital, SLLs and selective carbon-linked support.",
    }
    return f"{tier}: {commentary.get(subsector, 'Commercial rationale not set.')}"
