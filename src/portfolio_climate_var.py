"""Portfolio Climate Value-at-Risk (Climate VaR) model for Indian equity portfolios.

Methodology
-----------
Implements a scenario-based Climate VaR framework adapted for Indian capital markets.
Physical and transition risks are modelled separately and combined at the portfolio level.

Scenario Design
---------------
- **net_zero_2050**: Orderly 1.5°C pathway; early, steep carbon price ramp.
- **transition_2030**: Disorderly/delayed transition; carbon price shock concentrated
  in 2028-2030. India NDC-aligned.
- **physical_stress**: Chronic physical risk (heat stress, water scarcity, flooding)
  materialising by 2035 without significant transition.
- **baseline**: Current policies only; limited carbon pricing.

Sector Earnings Haircuts
-------------------------
Haircuts represent estimated earnings headwinds (as % of EBIT) under each scenario.
Based on IPCC AR6, IEA WEO 2024, NITI Aayog Net Zero report, and CRISIL research.
All values are illustrative scenario parameters — not investment forecasts.

Usage
-----
>>> from src.portfolio_climate_var import PortfolioClimateStress
>>> holdings = {"Energy": 0.18, "Materials": 0.12, "Financials": 0.25,
...             "IT": 0.20, "Consumer": 0.15, "Industrials": 0.10}
>>> stress = PortfolioClimateStress(holdings)
>>> results = stress.stress_test(scenario="transition_2030")
>>> print(results)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict

import pandas as pd


# ---------------------------------------------------------------------------
# Scenario parameters — earnings haircut by sector (% of EBIT)
# Sources: IEA WEO 2024, IPCC AR6, NITI Aayog Net Zero 2070, CRISIL
# ---------------------------------------------------------------------------

SCENARIO_SECTOR_HAIRCUTS: Dict[str, Dict[str, float]] = {
    "net_zero_2050": {
        "Energy": -0.35,
        "Materials": -0.28,
        "Utilities": -0.10,
        "Industrials": -0.18,
        "Consumer": -0.08,
        "IT": -0.02,
        "Financials": -0.06,
        "Healthcare": -0.03,
        "Real Estate": -0.12,
        "Communication": -0.02,
    },
    "transition_2030": {
        "Energy": -0.22,
        "Materials": -0.20,
        "Utilities": -0.08,
        "Industrials": -0.14,
        "Consumer": -0.06,
        "IT": -0.01,
        "Financials": -0.05,
        "Healthcare": -0.02,
        "Real Estate": -0.09,
        "Communication": -0.01,
    },
    "physical_stress": {
        "Energy": -0.12,
        "Materials": -0.16,
        "Utilities": -0.20,
        "Industrials": -0.10,
        "Consumer": -0.14,
        "IT": -0.04,
        "Financials": -0.08,
        "Healthcare": -0.05,
        "Real Estate": -0.18,
        "Communication": -0.03,
    },
    "baseline": {
        "Energy": -0.05,
        "Materials": -0.04,
        "Utilities": -0.03,
        "Industrials": -0.03,
        "Consumer": -0.02,
        "IT": 0.00,
        "Financials": -0.02,
        "Healthcare": -0.01,
        "Real Estate": -0.03,
        "Communication": 0.00,
    },
}

VALID_SCENARIOS = list(SCENARIO_SECTOR_HAIRCUTS.keys())


@dataclass
class PortfolioClimateStress:
    """Scenario-based climate stress test for an equity portfolio.

    Parameters
    ----------
    holdings : dict
        Sector weights as fractions summing to ~1.0.
        Keys must be GICS sector names matching SCENARIO_SECTOR_HAIRCUTS.
        Example: {"Energy": 0.18, "Materials": 0.12, "IT": 0.20, ...}
    pe_multiple : float
        Approximate P/E multiple used to convert earnings shock to price impact.
        Default 20x (approximate Nifty 50 long-run average).
    """

    holdings: Dict[str, float]
    pe_multiple: float = 20.0
    _validated_holdings: Dict[str, float] = field(init=False, repr=False)

    def __post_init__(self) -> None:
        total = sum(self.holdings.values())
        if not (0.95 <= total <= 1.05):
            raise ValueError(
                f"Holdings weights must sum to ~1.0, got {total:.3f}. "
                "Normalise before passing in."
            )
        unknown = set(self.holdings) - set(SCENARIO_SECTOR_HAIRCUTS["baseline"])
        if unknown:
            raise KeyError(
                f"Unknown sectors: {unknown}. "
                f"Valid sectors: {sorted(SCENARIO_SECTOR_HAIRCUTS['baseline'])}"
            )
        self._validated_holdings = self.holdings

    def stress_test(self, scenario: str = "transition_2030") -> pd.DataFrame:
        """Run a single-scenario climate stress test.

        Parameters
        ----------
        scenario : str
            One of: 'net_zero_2050', 'transition_2030', 'physical_stress', 'baseline'.

        Returns
        -------
        pd.DataFrame
            Sector-level and portfolio-level climate impact.
        """
        if scenario not in VALID_SCENARIOS:
            raise ValueError(f"Scenario '{scenario}' not found. Choose from {VALID_SCENARIOS}.")

        haircuts = SCENARIO_SECTOR_HAIRCUTS[scenario]
        rows = []
        for sector, weight in self._validated_holdings.items():
            haircut = haircuts[sector]
            price_impact = haircut * self.pe_multiple / (self.pe_multiple + 1)
            rows.append(
                {
                    "sector": sector,
                    "weight": round(weight, 4),
                    "earnings_haircut_pct": round(haircut * 100, 2),
                    "estimated_price_impact_pct": round(price_impact * 100, 2),
                    "weighted_portfolio_impact_pct": round(weight * price_impact * 100, 4),
                }
            )

        df = pd.DataFrame(rows).sort_values("weight", ascending=False).reset_index(drop=True)
        portfolio_impact = df["weighted_portfolio_impact_pct"].sum()
        summary_row = pd.DataFrame(
            [
                {
                    "sector": "PORTFOLIO TOTAL",
                    "weight": round(df["weight"].sum(), 4),
                    "earnings_haircut_pct": None,
                    "estimated_price_impact_pct": None,
                    "weighted_portfolio_impact_pct": round(portfolio_impact, 4),
                }
            ]
        )
        return pd.concat([df, summary_row], ignore_index=True)

    def stress_test_all_scenarios(self) -> pd.DataFrame:
        """Run stress tests across all scenarios and return a combined summary.

        Returns
        -------
        pd.DataFrame
            One row per scenario with portfolio-level Climate VaR estimate.
        """
        rows = []
        for scenario in VALID_SCENARIOS:
            result = self.stress_test(scenario)
            portfolio_row = result[result["sector"] == "PORTFOLIO TOTAL"].iloc[0]
            rows.append(
                {
                    "scenario": scenario,
                    "portfolio_climate_var_pct": portfolio_row["weighted_portfolio_impact_pct"],
                }
            )
        return pd.DataFrame(rows).sort_values("portfolio_climate_var_pct").reset_index(drop=True)
