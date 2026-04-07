# Green Bond Data

This folder contains data on India's green bond market.

## Files

### `issuance_history_synthetic.csv`
Synthetic/illustrative data representing the structure of the SEBI green bond issuance registry.
**This file uses plausible but fabricated values for schema demonstration.**
For real data, see the sources below.

Columns:
- `issuance_year` — Year of issuance
- `issuer_name` — Issuer entity
- `issuer_type` — `sovereign`, `psu`, `corporate`, `bank`
- `amount_inr_cr` — Issuance size in INR crore
- `tenor_years` — Bond tenor
- `coupon_pct` — Coupon rate
- `use_of_proceeds` — Primary category (e.g., `renewable_energy`, `green_buildings`)
- `external_review` — `second_party_opinion`, `certification`, `none`
- `listed_exchange` — `BSE`, `NSE`, `both`

### `pricing_spreads_synthetic.parquet`
Illustrative credit spread data vs. duration-matched vanilla bonds.
For real data, use Bloomberg or NSE/BSE bond analytics.

Columns:
- `isin` — Synthetic ISIN
- `issuer_name`
- `issue_date`
- `green_spread_bps` — Observed spread for the green bond
- `vanilla_matched_spread_bps` — Spread of a duration-matched vanilla bond from same issuer
- `greenium_bps` — Difference (negative = greenium, i.e. green trades tighter)

## Real Data Sources

| Source | URL | Coverage |
|--------|-----|----------|
| SEBI Green Bond Registry | https://www.sebi.gov.in | 2017–present |
| BSE Bond Platform | https://www.bseindia.com/markets/debt | Listed green bonds |
| NSE Debt Market | https://www.nseindia.com/market-data/bonds | NSE-listed bonds |
| CBI Green Bond Database | https://www.climatebonds.net/market/data | Global + India |
| Bloomberg (subscription) | — | Spreads, pricing, ratings |
