"""Bank positioning datasets and appendix helpers."""

from __future__ import annotations

import pandas as pd


def build_bank_positioning() -> pd.DataFrame:
    """Return the verified public bank-positioning comparison table."""

    return pd.DataFrame(
        [
            {
                "Bank": "Standard Chartered",
                "Verified public target / framework": "USD157bn mobilised Jan 2021-Sep 2025; USD300bn aspiration by 2030; green / sustainable and transition frameworks.",
                "India lens": "Strongest reviewed India-specific transition messaging; India survey and Apraava metering transaction are both public.",
                "Verified product strengths": "Green / project finance, green bonds and loans, SLLs, ESG-linked working capital, sustainable trade finance, blended platforms.",
                "Best-fit India use cases": "Renewables, grids, metering, EV ecosystems, distributed solar and FI on-lending platforms.",
                "Public note": "Cross-border and DFI-linked positioning is clearly visible from public materials.",
            },
            {
                "Bank": "Deutsche Bank",
                "Verified public target / framework": "EUR900bn cumulative target to YE2030; EUR471bn achieved by Q4 2025; Transition Finance Framework.",
                "India lens": "India transition and REC financing articles show project finance, AR, LC and ECB use cases in renewables.",
                "Verified product strengths": "Transition finance, project finance, SLLs, green bonds, trade and lending solutions.",
                "Best-fit India use cases": "Industrial decarbonisation, renewables refinancing, grid upgrades, NBFI lending platforms.",
                "Public note": "Strongest hard-to-abate positioning in the reviewed bank set.",
            },
            {
                "Bank": "UBS",
                "Verified public target / framework": "Sustainable Finance Guideline covers green, transition and sustainability-linked bonds and loans; 96 GSSS bond transactions in 2024.",
                "India lens": "UBS India highlights international capital-markets access; India-specific sustainable-lending positioning was not verified.",
                "Verified product strengths": "Green and transition bonds, sustainable loans, structured issuance, selective blended and carbon-linked capabilities.",
                "Best-fit India use cases": "Capital-markets-led refinancing, green buildings, mature clean-energy portfolios, advisory-led placements.",
                "Public note": "Analyst inference: strongest where advisory and investor distribution matter more than balance-sheet project lending.",
            },
        ]
    )


def build_bank_focus_matrix() -> pd.DataFrame:
    """Return the bank opportunity focus matrix."""

    return pd.DataFrame(
        [
            {
                "Bank": "Standard Chartered",
                "Renewables": "Lead: project finance + green bond take-out",
                "Grid / transmission": "Lead: project finance + DFI blend",
                "Storage / battery": "Lead with blended overlay",
                "Green buildings": "Selective: green loans / bonds",
                "Industrial decarb": "Selective: SLL + transition structures",
                "EV / mobility": "Lead: SLL + sustainable trade",
                "Working capital": "Lead",
                "FI / platforms": "Lead: on-lending and warehouse lines",
            },
            {
                "Bank": "Deutsche Bank",
                "Renewables": "Lead: project finance + refinancing",
                "Grid / transmission": "Lead: structured lending",
                "Storage / battery": "Selective: project / blended",
                "Green buildings": "Selective",
                "Industrial decarb": "Lead: transition finance + SLL",
                "EV / mobility": "Selective",
                "Working capital": "Lead: AR / LC / trade",
                "FI / platforms": "Lead: NBFI and REC-style lending",
            },
            {
                "Bank": "UBS",
                "Renewables": "Advisory-led: bonds / private placements",
                "Grid / transmission": "Advisory-led: green or transition bonds",
                "Storage / battery": "Selective: structured or private capital",
                "Green buildings": "Lead: green bond / green building funding",
                "Industrial decarb": "Selective: SLB / transition bond",
                "EV / mobility": "Selective: capital-markets-led",
                "Working capital": "Not verified as a public India strength",
                "FI / platforms": "Advisory / placement role",
            },
        ]
    )


def build_bank_plays() -> pd.DataFrame:
    """Return concrete bank-specific opportunity plays."""

    return pd.DataFrame(
        [
            {
                "bank": "Standard Chartered",
                "play": "Renewable and grid club deals with bond take-out",
                "products": "Green project finance, green bonds, blended finance",
                "client_types": "Developers, utilities, infrastructure funds",
                "why_now": "Verified project-finance, cross-border and DFI-linked positioning makes Standard Chartered well suited to own both construction debt and later refinancing.",
            },
            {
                "bank": "Standard Chartered",
                "play": "EV and charging ecosystem financing stack",
                "products": "SLLs, ESG-linked working capital, sustainable trade finance",
                "client_types": "Fleet operators, EPCs, OEM suppliers, charge-point operators",
                "why_now": "Standard Chartered explicitly markets sustainable trade finance and sustainability-linked solutions; EV ecosystems need both capex and short-dated liquidity.",
            },
            {
                "bank": "Standard Chartered",
                "play": "NBFC / FI clean-asset warehouse",
                "products": "Warehouse lines, green loans, future green securitisation, blended finance",
                "client_types": "NBFCs, banks, platform aggregators",
                "why_now": "Public materials show FI trade loans and blended-capital relevance, which fits fragmented rooftop solar and mobility pools.",
            },
            {
                "bank": "Deutsche Bank",
                "play": "Hard-to-abate transition finance program",
                "products": "Transition finance loans, SLLs, transition bonds",
                "client_types": "Steel, cement, chemicals and diversified industrial corporates",
                "why_now": "Deutsche Bank has the clearest publicly documented hard-to-abate transition framework of the three banks reviewed.",
            },
            {
                "bank": "Deutsche Bank",
                "play": "REC-style renewable lending and refinancing platform",
                "products": "Project finance, AR solutions, letters of credit, ECB loans, green bonds",
                "client_types": "NBFIs, developers, utilities",
                "why_now": "Its India renewables coverage explicitly references this financing mix, making it credible for Indian renewable platforms and lenders.",
            },
            {
                "bank": "Deutsche Bank",
                "play": "Storage and flexible-grid structured lending",
                "products": "Project finance, blended finance, working-capital bridges",
                "client_types": "Developers, utilities, EPCs",
                "why_now": "Its India transition and project-finance content both highlight storage need and capital intensity, supporting a structured-lending role.",
            },
            {
                "bank": "UBS",
                "play": "Green or transition bond franchise for mature Indian issuers",
                "products": "Green bonds, transition bonds, SLBs",
                "client_types": "Utilities, infrastructure funds, large corporates",
                "why_now": "Inference from UBS India, Investment Bank and sustainability reports: the best fit is labeled bond origination and investor distribution for mature portfolios.",
            },
            {
                "bank": "UBS",
                "play": "Private placement and structured issuance for operating clean-energy portfolios",
                "products": "Private placements, structured issuance, green bonds",
                "client_types": "Infrastructure funds, NBFCs, mature portfolio owners",
                "why_now": "UBS says it laid groundwork for green structured issuance; that reads as a capital-markets opportunity rather than a construction-lending one.",
            },
            {
                "bank": "UBS",
                "play": "Selective blended or carbon-linked advisory mandates",
                "products": "Blended finance, carbon-linked or removals-linked structures",
                "client_types": "Platform developers, industrial transition sponsors",
                "why_now": "UBS public materials mention blended finance and project-based carbon removals financing, but India execution should be treated as selective and advisory-led.",
            },
        ]
    )


def build_source_confidence_register(source_ledger: pd.DataFrame) -> pd.DataFrame:
    """Build a concise confidence register for the reviewed sources."""

    def confidence_level(row: pd.Series) -> str:
        title = str(row["publication_title"]).lower()
        if any(
            keyword in title
            for keyword in [
                "annual report",
                "sustainability report",
                "framework",
                "report supplement",
            ]
        ):
            return "High"
        if row["publication_date"] != "not verified":
            return "High"
        return "Medium"

    def treatment(row: pd.Series) -> str:
        if row["source_id"].startswith(("SC", "DB", "UBS")):
            return "Used for verified positioning or product evidence"
        return "Context only"

    register = source_ledger.copy()
    register["Confidence"] = register.apply(confidence_level, axis=1)
    register["Treatment"] = register.apply(treatment, axis=1)
    register["Coverage area"] = register["bank"] + " positioning / product evidence"
    return register[
        ["source_id", "bank", "publication_title", "Coverage area", "Confidence", "Treatment"]
    ].rename(
        columns={
            "source_id": "Source ID",
            "bank": "Bank",
            "publication_title": "Publication",
        }
    )


def build_opportunity_matrix_numeric(bank_focus_matrix: pd.DataFrame) -> pd.DataFrame:
    """Map qualitative bank focus strings to numeric heatmap values."""

    mapping = {
        "lead": 4.0,
        "advisory-led": 3.0,
        "selective": 2.0,
        "advisory": 2.5,
        "not verified": 0.5,
    }

    numeric = bank_focus_matrix.set_index("Bank").copy()
    for column in numeric.columns:
        numeric[column] = numeric[column].map(
            lambda value: _extract_focus_value(str(value), mapping)
        )
    return numeric


def _extract_focus_value(value: str, mapping: dict[str, float]) -> float:
    lower = value.lower()
    for key, score in mapping.items():
        if lower.startswith(key):
            return score
    return 1.5
