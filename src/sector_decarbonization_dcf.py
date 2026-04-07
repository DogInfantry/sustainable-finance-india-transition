"""Sector decarbonisation DCF and capex modelling for hard-to-abate sectors.

Methodology
-----------
Models the NPV of decarbonisation investment for cement, steel, and coal power
sectors under varying carbon price assumptions.

Key assumptions and sources are documented as module-level constants.
All values are scenario assumptions for analytical purposes — not forecasts.

Sectors Covered
---------------
- **Cement**: Fuel switching + clinker substitution + CCS readiness
- **Steel**: Scrap-based EAF, hydrogen DRI transition economics
- **Coal Power**: Plant retirement sequencing, refinancing gap modelling

Carbon Price Scenarios (INR/tonne CO2)
---------------------------------------
- Low:    ₹1,500  (current voluntary carbon market levels, 2024)
- Mid:    ₹3,000  (SEBI/MoEFCC working estimates for 2028 compliance)
- High:   ₹5,000  (NITI Aayog net-zero pathway 2030 carbon cost)
- Stress: ₹8,000  (EU-carbon-price parity scenario)

Sources
-------
- CRISIL Transition Finance report (2023)
- IEA Steel Technology Roadmap (2024)
- Global Cement and Concrete Association net-zero roadmap
- NITI Aayog Low Carbon Development Strategy (2022)
- RBI Discussion Paper on Climate Risk (2023)

Usage
-----
>>> from src.sector_decarbonization_dcf import SectorDCF
>>> dcf = SectorDCF(sector='cement', technology='clinker_substitution')
>>> result = dcf.run_valuation(capex_year=2025, carbon_price=5000)
>>> print(result)
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Tuple

import pandas as pd


# ---------------------------------------------------------------------------
# Sector + technology parameter library
# Units: capex in INR crore per unit, abatement in tCO2/unit/year
# ---------------------------------------------------------------------------

SECTOR_TECH_PARAMS: Dict[str, Dict[str, dict]] = {
    "cement": {
        "clinker_substitution": {
            "capex_inr_cr": 150,
            "annual_opex_savings_inr_cr": 20,
            "abatement_tco2_per_year": 85_000,
            "useful_life_years": 15,
            "description": "Blended cement with fly ash / GGBS; lowers clinker ratio from ~0.8 to ~0.65",
        },
        "fuel_switching": {
            "capex_inr_cr": 280,
            "annual_opex_savings_inr_cr": 35,
            "abatement_tco2_per_year": 120_000,
            "useful_life_years": 20,
            "description": "Replace coal kilns with alternative fuel (AFR/biomass) systems",
        },
        "ccs_readiness": {
            "capex_inr_cr": 950,
            "annual_opex_savings_inr_cr": -30,
            "abatement_tco2_per_year": 400_000,
            "useful_life_years": 25,
            "description": "Post-combustion CCS; high capex, dependent on carbon price above ₹6,000",
        },
    },
    "steel": {
        "scrap_eaf": {
            "capex_inr_cr": 450,
            "annual_opex_savings_inr_cr": 60,
            "abatement_tco2_per_year": 550_000,
            "useful_life_years": 20,
            "description": "Electric arc furnace using scrap steel; ~75% lower emissions vs BF-BOF",
        },
        "hydrogen_dri": {
            "capex_inr_cr": 1_800,
            "annual_opex_savings_inr_cr": -80,
            "abatement_tco2_per_year": 800_000,
            "useful_life_years": 25,
            "description": "Green hydrogen-based DRI; near-zero steel pathway; high capex, opex-heavy",
        },
    },
    "coal_power": {
        "plant_retirement_refinancing": {
            "capex_inr_cr": 0,
            "annual_opex_savings_inr_cr": 40,
            "abatement_tco2_per_year": 1_200_000,
            "useful_life_years": 0,
            "description": "Early retirement of sub-critical coal plant; savings from avoided fuel cost",
        },
        "renewable_replacement": {
            "capex_inr_cr": 600,
            "annual_opex_savings_inr_cr": 55,
            "abatement_tco2_per_year": 900_000,
            "useful_life_years": 25,
            "description": "Replace retired coal capacity with utility-scale solar + storage",
        },
    },
}

CARBON_PRICE_SCENARIOS: Dict[str, int] = {
    "low": 1_500,
    "mid": 3_000,
    "high": 5_000,
    "stress": 8_000,
}

DEFAULT_DISCOUNT_RATE = 0.12  # 12% WACC — typical Indian infra project


@dataclass
class SectorDCF:
    """Decarbonisation DCF model for hard-to-abate Indian sectors.

    Parameters
    ----------
    sector : str
        One of: 'cement', 'steel', 'coal_power'.
    technology : str
        Technology pathway within the sector. See SECTOR_TECH_PARAMS.
    discount_rate : float
        WACC for NPV discounting. Default 12%.
    """

    sector: str
    technology: str
    discount_rate: float = DEFAULT_DISCOUNT_RATE

    def __post_init__(self) -> None:
        if self.sector not in SECTOR_TECH_PARAMS:
            raise ValueError(
                f"Sector '{self.sector}' not found. "
                f"Available: {list(SECTOR_TECH_PARAMS)}"
            )
        if self.technology not in SECTOR_TECH_PARAMS[self.sector]:
            raise ValueError(
                f"Technology '{self.technology}' not found for sector '{self.sector}'. "
                f"Available: {list(SECTOR_TECH_PARAMS[self.sector])}"
            )
        self._params = SECTOR_TECH_PARAMS[self.sector][self.technology]

    def run_valuation(
        self,
        capex_year: int = 2025,
        carbon_price: int = 5_000,
    ) -> pd.DataFrame:
        """Run the decarbonisation DCF and return a year-by-year cashflow table.

        Parameters
        ----------
        capex_year : int
            Year in which capex is deployed (year 0).
        carbon_price : int
            Carbon price in INR per tonne CO2 used to value abatement.

        Returns
        -------
        pd.DataFrame
            Annual cashflows, NPV, and payback details.
        """
        p = self._params
        life = p["useful_life_years"]

        if life == 0:
            # Retirement / no-capex case
            return self._retirement_case(capex_year, carbon_price)

        carbon_value_annual = (p["abatement_tco2_per_year"] * carbon_price) / 1e7  # INR cr
        annual_benefit = p["annual_opex_savings_inr_cr"] + carbon_value_annual
        capex = p["capex_inr_cr"]

        rows = []
        npv_cumulative = -capex
        for year_offset in range(1, life + 1):
            year = capex_year + year_offset
            discount_factor = 1 / (1 + self.discount_rate) ** year_offset
            pv_benefit = annual_benefit * discount_factor
            npv_cumulative += pv_benefit
            rows.append(
                {
                    "year": year,
                    "year_offset": year_offset,
                    "annual_benefit_inr_cr": round(annual_benefit, 2),
                    "discount_factor": round(discount_factor, 4),
                    "pv_benefit_inr_cr": round(pv_benefit, 2),
                    "cumulative_npv_inr_cr": round(npv_cumulative, 2),
                }
            )

        df = pd.DataFrame(rows)
        df.attrs["capex_inr_cr"] = capex
        df.attrs["terminal_npv_inr_cr"] = round(npv_cumulative, 2)
        df.attrs["carbon_price_inr_tonne"] = carbon_price
        df.attrs["technology"] = self.technology
        df.attrs["sector"] = self.sector
        return df

    def npv_by_carbon_price(
        self,
        capex_year: int = 2025,
        scenarios: Dict[str, int] | None = None,
    ) -> pd.DataFrame:
        """Return NPV across multiple carbon price scenarios.

        Parameters
        ----------
        capex_year : int
            Year of capex deployment.
        scenarios : dict, optional
            Carbon price scenario dict {name: INR/tonne}.
            Defaults to CARBON_PRICE_SCENARIOS.

        Returns
        -------
        pd.DataFrame
            Scenario name, carbon price, and terminal NPV.
        """
        scenarios = scenarios or CARBON_PRICE_SCENARIOS
        rows = []
        for name, price in scenarios.items():
            dcf = self.run_valuation(capex_year=capex_year, carbon_price=price)
            npv = dcf.attrs.get("terminal_npv_inr_cr", dcf["cumulative_npv_inr_cr"].iloc[-1])
            rows.append(
                {
                    "scenario": name,
                    "carbon_price_inr_tonne": price,
                    "terminal_npv_inr_cr": round(npv, 2),
                    "viable": npv >= 0,
                }
            )
        return pd.DataFrame(rows)

    def _retirement_case(
        self, capex_year: int, carbon_price: int
    ) -> pd.DataFrame:
        """Special case for coal plant retirement (zero capex, immediate abatement value)."""
        p = self._params
        carbon_value_annual = (p["abatement_tco2_per_year"] * carbon_price) / 1e7
        annual_benefit = p["annual_opex_savings_inr_cr"] + carbon_value_annual
        rows = []
        npv = 0.0
        for year_offset in range(1, 21):  # 20-year horizon for retirement
            year = capex_year + year_offset
            df_factor = 1 / (1 + self.discount_rate) ** year_offset
            pv = annual_benefit * df_factor
            npv += pv
            rows.append(
                {
                    "year": year,
                    "year_offset": year_offset,
                    "annual_benefit_inr_cr": round(annual_benefit, 2),
                    "discount_factor": round(df_factor, 4),
                    "pv_benefit_inr_cr": round(pv, 2),
                    "cumulative_npv_inr_cr": round(npv, 2),
                }
            )
        result = pd.DataFrame(rows)
        result.attrs["terminal_npv_inr_cr"] = round(npv, 2)
        result.attrs["carbon_price_inr_tonne"] = carbon_price
        return result
