"""ESG factor extraction and credit spread attribution for Indian fixed income.

Methodology
-----------
Estimates the credit spread component attributable to ESG factors using a
quartile-based spread differential approach.

For each ESG quartile bucket (Q1 = best, Q4 = worst), we estimate the
basis-point premium demanded by the market relative to the Q1 benchmark.
This is a simplified attribution — in practice, spread differentials
should be controlled for duration, rating, sector, and liquidity.

Data Basis
----------
Spread differentials below are calibrated to Indian corporate bond universe
(CRISIL-rated, listed on BSE/NSE). Values are illustrative scenario
parameters derived from analyst estimates and BRSR disclosure patterns.
Actual differentials require regression on live spread data.

Sources
-------
- CRISIL ESG Scores and Indian corporate bond spreads (2022–2024)
- SEBI BRSR disclosure analysis
- MSCI ESG Research India universe

Usage
-----
>>> from src.esg_credit_spread_model import ESGSpreadAttributor
>>> attributor = ESGSpreadAttributor()
>>> df = attributor.attribution_table()
>>> print(df)

>>> spread = attributor.estimate_spread(esg_score=42.0, base_spread_bps=180.0)
>>> print(f"Estimated spread: {spread:.1f} bps")
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List

import pandas as pd


# ---------------------------------------------------------------------------
# ESG quartile spread differential parameters (basis points)
# Source: Illustrative calibration based on CRISIL research and BRSR data
# ---------------------------------------------------------------------------

ESG_QUARTILE_PARAMS: List[dict] = [
    {
        "quartile": "Q1 (Best, score 75–100)",
        "score_min": 75,
        "score_max": 100,
        "spread_premium_bps": 0,
        "description": "Best-in-class ESG. Full BRSR disclosure, low transition risk.",
    },
    {
        "quartile": "Q2 (score 50–74)",
        "score_min": 50,
        "score_max": 74,
        "spread_premium_bps": 12,
        "description": "Above-average ESG. Partial BRSR, sector-level risks manageable.",
    },
    {
        "quartile": "Q3 (score 25–49)",
        "score_min": 25,
        "score_max": 49,
        "spread_premium_bps": 28,
        "description": "Below-average ESG. Material gaps in disclosure; sector exposure elevated.",
    },
    {
        "quartile": "Q4 (Worst, score 0–24)",
        "score_min": 0,
        "score_max": 24,
        "spread_premium_bps": 55,
        "description": "Weak ESG profile. High transition/physical risk, low disclosure quality.",
    },
]


@dataclass
class ESGSpreadAttributor:
    """Estimate and attribute credit spread to ESG factor quartiles.

    Parameters
    ----------
    quartile_params : list of dict, optional
        Override default ESG quartile parameters. Each dict must contain
        'score_min', 'score_max', and 'spread_premium_bps'.
    """

    quartile_params: List[dict] | None = None

    def __post_init__(self) -> None:
        self._params = self.quartile_params or ESG_QUARTILE_PARAMS

    def attribution_table(self) -> pd.DataFrame:
        """Return the full ESG quartile spread attribution table.

        Returns
        -------
        pd.DataFrame
            Quartile, score range, spread premium, and description.
        """
        return pd.DataFrame(self._params)

    def estimate_spread(self, esg_score: float, base_spread_bps: float) -> float:
        """Estimate total credit spread including ESG premium.

        Parameters
        ----------
        esg_score : float
            ESG score between 0 and 100.
        base_spread_bps : float
            Baseline credit spread in basis points (non-ESG component).

        Returns
        -------
        float
            Estimated total spread including ESG premium, in basis points.

        Raises
        ------
        ValueError
            If esg_score is outside [0, 100].
        """
        if not (0 <= esg_score <= 100):
            raise ValueError(f"ESG score must be between 0 and 100, got {esg_score}.")

        premium = self._get_premium(esg_score)
        return round(base_spread_bps + premium, 2)

    def _get_premium(self, esg_score: float) -> float:
        for bucket in self._params:
            if bucket["score_min"] <= esg_score <= bucket["score_max"]:
                return float(bucket["spread_premium_bps"])
        return 0.0

    def score_sensitivity(
        self, base_spread_bps: float, score_range: tuple[int, int] = (0, 100), steps: int = 21
    ) -> pd.DataFrame:
        """Return spread estimates across a range of ESG scores.

        Parameters
        ----------
        base_spread_bps : float
            Non-ESG component of the credit spread.
        score_range : tuple of int
            (min_score, max_score) range to evaluate.
        steps : int
            Number of score steps.

        Returns
        -------
        pd.DataFrame
            ESG score, ESG premium, and total spread.
        """
        import numpy as np

        scores = np.linspace(score_range[0], score_range[1], steps)
        rows = []
        for score in scores:
            premium = self._get_premium(score)
            rows.append(
                {
                    "esg_score": round(score, 1),
                    "esg_premium_bps": premium,
                    "total_spread_bps": round(base_spread_bps + premium, 2),
                }
            )
        return pd.DataFrame(rows)
