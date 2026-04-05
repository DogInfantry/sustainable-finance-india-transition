"""Lifecycle financing model: product evolution across development stages."""
from __future__ import annotations

import pandas as pd

from src.constants import (
    LIFECYCLE_STAGES,
    PRODUCT_CATEGORY_MAP,
    REPORTS_DIR,
    SUBSECTORS,
)

LIFECYCLE_DATA: dict[str, dict[str, dict[str, str]]] = {
    "Solar Utility-Scale": {
        "Development":  {"primary": "Development Loan",      "secondary": "Equity Bridge",            "rationale": "Pre-PPA risk; short-tenor development facility"},
        "Construction": {"primary": "Green Project Finance", "secondary": "Blended Finance",          "rationale": "Senior secured; DFI co-lending common at scale"},
        "Operation":    {"primary": "Green Bond",            "secondary": "SLL Refinancing",          "rationale": "Stable cashflow enables bond market access"},
        "Refinancing":  {"primary": "SLL Refinancing",       "secondary": "Green Bond Tap",           "rationale": "Rate optimisation; ESG KPI linkage adds pricing benefit"},
    },
    "Wind Onshore": {
        "Development":  {"primary": "Development Loan",      "secondary": "Equity Bridge",            "rationale": "Site development and permitting phase"},
        "Construction": {"primary": "Green Project Finance", "secondary": "DFI Co-lending",           "rationale": "Senior secured; multilateral co-lending available"},
        "Operation":    {"primary": "Green Bond",            "secondary": "Term Loan",                "rationale": "Long-tenor stable cashflow; bond execution viable"},
        "Refinancing":  {"primary": "SLL Refinancing",       "secondary": "Green Bond Tap",           "rationale": "Optimise cost of capital with sustainability linkage"},
    },
    "Wind Offshore": {
        "Development":  {"primary": "Development Loan",      "secondary": "Mezzanine Loan",           "rationale": "High complexity; mezzanine often required for risk layering"},
        "Construction": {"primary": "Blended Finance",       "secondary": "Green Project Finance",    "rationale": "Nascent market; concessional capital essential"},
        "Operation":    {"primary": "Green Project Finance", "secondary": "Green Bond",               "rationale": "Track record builds before bond market access"},
        "Refinancing":  {"primary": "Green Bond",            "secondary": "SLL Refinancing",          "rationale": "Refinancing onto bond market as asset class matures"},
    },
    "Battery Storage": {
        "Development":  {"primary": "Development Loan",      "secondary": "Equity Bridge",            "rationale": "Technology and offtake risk managed at development stage"},
        "Construction": {"primary": "Green Project Finance", "secondary": "Partial Credit Guarantee", "rationale": "PCG from DFIs increasingly used to enhance bankability"},
        "Operation":    {"primary": "SLL",                   "secondary": "Green Bond",               "rationale": "SLL suitable given measurable storage/grid KPIs"},
        "Refinancing":  {"primary": "Green Bond",            "secondary": "SLL Refinancing",          "rationale": "Bond market access as storage asset class matures"},
    },
    "EV Charging Infrastructure": {
        "Development":  {"primary": "Working Capital Facility", "secondary": "Development Loan",      "rationale": "Fragmented, asset-light; working capital more relevant"},
        "Construction": {"primary": "Green Project Finance",    "secondary": "Blended Finance",       "rationale": "Anchor sites project-financed; DFI support for network buildout"},
        "Operation":    {"primary": "SLL",                      "secondary": "Revolving Credit Facility", "rationale": "SLL with utilisation/uptime KPIs"},
        "Refinancing":  {"primary": "Sustainability Bond",      "secondary": "SLL Refinancing",       "rationale": "Portfolio aggregation enables bond market access"},
    },
    "Green Buildings": {
        "Development":  {"primary": "Development Loan",      "secondary": "Equity Bridge",            "rationale": "Developer finance at pre-construction stage"},
        "Construction": {"primary": "Green Project Finance", "secondary": "Concessional Tranche",     "rationale": "Green certification unlocks preferential pricing"},
        "Operation":    {"primary": "Sustainability Bond",   "secondary": "SLL",                      "rationale": "Portfolio of certified buildings suitable for sustainability bond"},
        "Refinancing":  {"primary": "SLL Refinancing",       "secondary": "Green Bond Tap",           "rationale": "Ongoing green certification metrics link to margin ratchets"},
    },
    "Industrial Decarbonisation": {
        "Development":  {"primary": "Working Capital Facility", "secondary": "Development Loan",      "rationale": "Technology assessment and feasibility; corporate credit-backed"},
        "Construction": {"primary": "SLL",                      "secondary": "Green Project Finance", "rationale": "SLL against decarbonisation KPIs; PF for discrete capex"},
        "Operation":    {"primary": "Transition Bond",          "secondary": "SLL",                   "rationale": "Transition bond framework appropriate for hard-to-abate sector"},
        "Refinancing":  {"primary": "Sustainability Bond",      "secondary": "SLL Refinancing",       "rationale": "Refinancing as decarbonisation pathway matures"},
    },
    "Circular Economy": {
        "Development":  {"primary": "Development Loan",      "secondary": "Concessional Tranche",     "rationale": "Thin track record; concessional tranche often needed"},
        "Construction": {"primary": "Blended Finance",       "secondary": "Green Project Finance",    "rationale": "DFI/blended finance essential given nascent viability"},
        "Operation":    {"primary": "Green Bond",            "secondary": "SLL",                      "rationale": "Operating asset; green bond if use-of-proceeds clear"},
        "Refinancing":  {"primary": "SLL Refinancing",       "secondary": "Sustainability Bond",      "rationale": "SLL with circularity metrics for refinancing phase"},
    },
    "Transmission & Grid": {
        "Development":  {"primary": "Development Loan",      "secondary": "Guarantee",                "rationale": "Regulated utility; government guarantee reduces dev debt cost"},
        "Construction": {"primary": "Green Project Finance", "secondary": "DFI Co-lending",           "rationale": "Large-ticket senior secured; multilateral co-lending common"},
        "Operation":    {"primary": "Green Bond",            "secondary": "Sustainability Bond",      "rationale": "Regulated cashflow ideal for long-duration bond"},
        "Refinancing":  {"primary": "Green Bond Tap",        "secondary": "SLL Refinancing",          "rationale": "Tap existing green bond programme; SLL where grid KPIs measurable"},
    },
}


def build_lifecycle_matrix() -> pd.DataFrame:
    """Returns DataFrame[subsector, stage, primary_product, secondary_product, rationale].

    Validates:
    - All SUBSECTORS present
    - All LIFECYCLE_STAGES present per subsector
    - All product strings exist in PRODUCT_CATEGORY_MAP
    """
    rows = []
    for sub in SUBSECTORS:
        for stage in LIFECYCLE_STAGES:
            cell = LIFECYCLE_DATA[sub][stage]
            rows.append({
                "subsector":        sub,
                "stage":            stage,
                "primary_product":  cell["primary"],
                "secondary_product": cell["secondary"],
                "rationale":        cell["rationale"],
            })

    df = pd.DataFrame(rows)

    # Validate all products in PRODUCT_CATEGORY_MAP
    for col in ("primary_product", "secondary_product"):
        unknown = set(df[col]) - set(PRODUCT_CATEGORY_MAP.keys())
        if unknown:
            raise ValueError(f"Products not in PRODUCT_CATEGORY_MAP ({col}): {unknown}")

    return df


def export_lifecycle_matrix(
    output_path: str = f"{REPORTS_DIR}/lifecycle_financing_matrix.csv",
) -> pd.DataFrame:
    """Write lifecycle matrix to CSV and return DataFrame."""
    df = build_lifecycle_matrix()
    df.to_csv(output_path, index=False)
    return df
