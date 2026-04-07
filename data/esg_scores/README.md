# ESG Scores Data

This folder contains ESG scoring data for Indian equities.

## Files

### `nifty50_esg_metrics_synthetic.csv`
Illustrative ESG metrics for a representative subset of Nifty 50 constituents.
**Values are synthetic and for schema/model demonstration only.**
For real ESG scores, use MSCI ESG Research, Sustainalytics, or company BRSR filings.

Columns:
- `ticker` — NSE ticker
- `company_name`
- `sector` — GICS sector
- `environmental_score` — 0–100
- `social_score` — 0–100
- `governance_score` — 0–100
- `composite_esg_score` — Weighted composite (E: 40%, S: 30%, G: 30%)
- `brsr_disclosed` — Boolean; whether company has filed BRSR
- `brsr_quality` — `full`, `partial`, `none`
- `thermal_coal_exposure_pct` — Revenue % from thermal coal
- `water_stress_flag` — Boolean; operations in high water-stress zones

### `sector_benchmarks_synthetic.csv`
Sector-level ESG percentile benchmarks for the Nifty 50 universe.

## Real Data Sources

| Source | Coverage | Access |
|--------|----------|--------|
| SEBI BRSR Filings | Nifty 1000 mandatory | NSE/BSE XBRL portal |
| MSCI ESG Research | Global + India | Subscription |
| Sustainalytics | Global + India | Subscription |
| Bloomberg ESG | Nifty 50+ | Subscription |
| BSE Sustainability Reports | Self-disclosed | Free (BSE portal) |
