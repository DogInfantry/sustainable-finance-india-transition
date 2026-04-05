<div align="center">

# 🌿 Sustainable Finance — India Transition

**Original research on India's green bond markets, ESG frameworks, climate risk modeling,
SEBI/RBI policy analysis, and transition finance for hard-to-abate sectors.**

[![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-22c55e?style=for-the-badge)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-22c55e?style=for-the-badge)]()
[![Market](https://img.shields.io/badge/Market-India-FF9933?style=for-the-badge)]()

> Bridging SEBI/RBI regulatory intent, Indian capital market structure, and climate-aligned
> capital allocation — with data, original frameworks, and quantitative models.

[📗 Green Bonds](#-green-bond-markets) · [📊 ESG Integration](#-esg-data--integration) · [🌡️ Climate Risk](#️-climate-risk-modeling) · [🏛️ Policy](#️-sebi--rbi-policy) · [⚙️ Transition Finance](#️-transition-finance)

</div>

---

## ⚡ Scope at a Glance

| Domain | Coverage | Key Output |
|--------|----------|------------|
| 🟢 **Green Bonds** | Sovereign, corporate & PSU issuance · 2015–present | Spread attribution vs. vanilla bonds; valuation model |
| 📊 **ESG Integration** | Nifty 50 + selected mid-cap universe | Weighted scoring model; sector benchmarks; data gap analysis |
| 🌡️ **Climate Risk** | Agriculture, power, infra, auto, cement | Portfolio Climate VaR; transition scenario stress tests |
| 🏛️ **SEBI / RBI Policy** | BRSR, green deposit frameworks, RBI circulars | Policy timeline; implementation gap analysis |
| ⚙️ **Transition Finance** | Cement, steel, coal power | Decarbonization capex DCF; SLB/transition bond structuring |

---

## 📗 Green Bond Markets

Analysis of India's green bond ecosystem — issuance trends, pricing mechanics, and credit spread attribution across sovereign, PSU, and corporate issuers.

- Green bond issuance history by year, sector, and issuer type (SEBI registry data)
- Spread attribution vs. duration-matched vanilla bonds — liquidity, coupon, and greenium effects
- Eligibility framework mapping (SEBI green bond guidelines + external review process)
- Investor participation breakdown: FIIs, domestic institutions, retail

**Key Finding:** Green bonds trade tighter than vanilla bonds on a duration-adjusted basis, signalling institutional appetite — but end-use verification and impact measurement remain structurally weak.

---

## 📊 ESG Data & Integration

Original frameworks for ESG integration in Indian equity and debt markets, addressing the data gaps specific to emerging market universes.

- ESG data coverage analysis: mid/small-cap universe <40% disclosed
- Sector-specific metrics: thermal coal exposure, water stress in manufacturing, governance flags
- Weighted ESG scoring model for Nifty 50 constituents
- Fixed income ESG overlay: credit spread attribution to ESG factor quartiles
- Case study: Nifty 50 ESG integration; SOE transition readiness assessment

**Key Finding:** No significant correlation between ESG score and returns in Indian equities yet — but sector bifurcation is pronounced: IT/pharma vs. metals/mining show a 70+ percentile gap on environmental scores.

---

## 🌡️ Climate Risk Modeling

Quantitative stress testing for physical and transition climate risks across Indian capital markets.

- Climate risk taxonomy: physical (rainfall, flooding, heat stress) vs. transition (carbon pricing, tech disruption)
- Sector stress tests: agriculture, power, infrastructure, auto, cement
- Portfolio Climate VaR under 1.5°C, 2°C, and delayed-transition scenarios
- Fixed income spread scenarios: basis-point moves under carbon policy shocks
- India-specific scenario design: net-zero 2070 pathway, sectoral emissions caps

**Key Finding:** Under a 2°C transition scenario (carbon price ₹5,000/tonne by 2030), energy and materials sectors face 15–25% earnings headwinds. Indian equity markets show no climate risk premium yet — alpha opportunity for climate-informed positioning.

---

## 🏛️ SEBI & RBI Policy

Timeline, implementation mechanics, and gap analysis of India's sustainable finance regulatory architecture.

- **SEBI BRSR** — evolution from voluntary to mandatory; disclosure quality assessment
- **RBI Climate Risk Circular** — principles-based guidance; enforcement timeline uncertainty
- Green deposit frameworks and ESG lending guidelines
- International alignment: TCFD, EU Taxonomy comparisons
- Implementation gaps: data standardisation, third-party verification, enforcement capacity

**Key Finding:** SEBI's BRSR rollout is structurally comprehensive but enforcement is nascent. RBI guidance is principles-based, not rules-based — creating compliance ambiguity for regulated entities.

---

## ⚙️ Transition Finance

Structuring frameworks and financial models for decarbonisation of hard-to-abate sectors in India.

- Sector decarbonisation pathways:
  - **Cement** — fuel switching, clinker substitution, CCS readiness
  - **Steel** — scrap-based EAF, hydrogen DRI transition economics
  - **Coal Power** — plant retirement sequencing, refinancing gap modelling
- Instrument design: transition bonds, SLBs, sustainability-linked loans, green project finance
- Capex requirement models, IRR sensitivity to carbon price
- Carbon economics: cost of abatement, carbon credit value, competitive impact
- Case studies: PSU power plant retirement + renewable refinancing; cement kiln modernisation

**Key Finding:** Cement sector decarbonisation cost is ₹8–12 per unit — viable within margin structure if carbon price exceeds ₹3,000/tonne. Green-linked bond uptake is limited by KPI verification burden.

---

## 🗂️ Repository Structure

```
sustainable-finance-india-transition/
│
├── 📁 data/
│   ├── green_bonds/
│   │   ├── issuance_history.csv          # SEBI green bond registry (2015–present)
│   │   └── pricing_spreads.parquet       # Credit spreads vs. vanilla bonds
│   ├── esg_scores/
│   │   ├── nifty50_esg_metrics.csv       # Company-level ESG scoring
│   │   └── sector_benchmarks.csv         # Sector ESG percentiles
│   ├── climate_scenarios/
│   │   ├── india_net_zero_2070.json      # Policy scenario parameters
│   │   └── sector_emissions.parquet      # Baseline & transition emissions
│   └── policy_docs/
│       ├── sebi_brsr_guidelines.pdf
│       └── rbi_climate_risk_circular.pdf
│
├── 📁 notebooks/                          # Jupyter analysis workflows
├── 📁 src/                                # Python models & scoring engines
│   ├── portfolio_climate_var.py          # Equity portfolio climate stress test
│   ├── sector_decarbonization_dcf.py     # Capex & IRR modelling
│   └── esg_credit_spread_model.py        # Fixed income ESG factor extraction
└── 📁 reports/                            # Formatted research outputs
```

---

## 🚀 Quick Start

```bash
git clone https://github.com/DogInfantry/sustainable-finance-india-transition.git
cd sustainable-finance-india-transition
pip install -r requirements.txt
```

```python
import pandas as pd, json

# Green bond data
gb = pd.read_csv('data/green_bonds/issuance_history.csv')
spreads = pd.read_parquet('data/green_bonds/pricing_spreads.parquet')

# ESG metrics
esg = pd.read_csv('data/esg_scores/nifty50_esg_metrics.csv')

# Climate scenarios
with open('data/climate_scenarios/india_net_zero_2070.json') as f:
    scenarios = json.load(f)
```

```python
# Run climate stress test
from src.portfolio_climate_var import PortfolioClimateStress
results = PortfolioClimateStress(holdings, esg_ratings).stress_test(scenario='transition_2030')

# Sector decarbonisation DCF
from src.sector_decarbonization_dcf import SectorDCF
npv = SectorDCF(sector='cement', technology='clinker_substitution').run_valuation(capex_year=2025, carbon_price=5000)
```

---

## 🗃️ Data Sources

| Dataset | Source | Coverage |
|---------|--------|----------|
| Green bond issuance | SEBI, BSE, NSE | 2015–present |
| ESG scores | MSCI, Bloomberg, company BRSR filings | Nifty 50 + selected mid-cap |
| Climate scenarios | IEA, NITI Aayog, World Bank | India-specific pathways |
| Policy documents | SEBI, RBI, MoEFCC | Latest circulars |
| Emissions data | CRISIL, company disclosures | Hard-to-abate sectors |

---

## ⚠️ Limitations

- **ESG data quality** — relies on company self-disclosure; cross-provider inconsistency is common
- **Scenario uncertainty** — climate pathways carry deep uncertainty; outputs are illustrative
- **Model sensitivity** — transition finance models are highly sensitive to capex profiles and carbon price assumptions
- **Regulatory evolution** — SEBI/RBI frameworks are actively evolving; analysis may not reflect latest circulars
- *Not investment advice — for educational and analytical purposes only*

---

## 🔗 Related Repositories

| Repository | Focus |
|------------|-------|
| [capital-markets-intelligence](https://github.com/DogInfantry/capital-markets-intelligence) | IPO event studies, M&A screening, sovereign risk index, yield curve decomposition |
| [investment-risk-management-console](https://github.com/DogInfantry/investment-risk-management-console) | Real-time Nifty 50 risk dashboard, stress testing, sector attribution |
| [critical-minerals-green-steel](https://github.com/DogInfantry/critical-minerals-green-steel) | India minerals policy, green steel industrial transition |

---

## 📜 License

MIT License — see [LICENSE](LICENSE). Attribution appreciated.

---

<div align="center">

**Last Updated:** April 2026 &nbsp;·&nbsp; **Status:** 🟢 Active &nbsp;·&nbsp; **Market Focus:** India

*Original research · No API keys required · Built for practitioners*

</div>
