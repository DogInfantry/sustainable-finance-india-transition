<div align="center">

# 🌿 Sustainable Finance — India Transition

**Original research on India's green bond markets, ESG frameworks, climate risk modeling,
SEBI/RBI policy analysis, transition finance for hard-to-abate sectors, and a commercial strategy engine for sustainable finance practitioners.**

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![CI](https://img.shields.io/github/actions/workflow/status/DogInfantry/sustainable-finance-india-transition/ci.yml?branch=main&style=for-the-badge&label=CI)](https://github.com/DogInfantry/sustainable-finance-india-transition/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-22c55e?style=for-the-badge)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-22c55e?style=for-the-badge)]()
[![Market](https://img.shields.io/badge/Market-India-FF9933?style=for-the-badge)]()

> Bridging SEBI/RBI regulatory intent, Indian capital market structure, and climate-aligned
> capital allocation — with data, original frameworks, quantitative models, and a bank strategy engine.

[📗 Green Bonds](#-green-bond-markets) · [📊 ESG](#-esg-data--integration) · [🌡️ Climate Risk](#️-climate-risk-modeling) · [🏛️ Policy](#️-sebi--rbi-policy) · [⚙️ Transition Finance](#️-transition-finance) · [🏦 Commercial Layer](#-commercial-strategy-layer) · [🚀 Run It](#-quick-start)

</div>

---

## ✦ What Makes This Different

| Principle | How It's Applied |
|-----------|------------------|
| **Verified-only bank claims** | All bank positioning sourced exclusively from official public materials — annual reports, sustainability frameworks, press releases. Unverified gaps explicitly marked `not verified`. |
| **Single-command reproducibility** | `python build.py` regenerates all reports, figures, and appendix tables from source data — no manual steps. |
| **Rule-based transparency** | Product recommendations use explicit, explainable scoring criteria. Every weight is inspectable in `src/taxonomy.py` and `config/priority_weights.yaml`. |
| **CI-enforced integrity** | GitHub Actions runs tests and rebuilds outputs on every push and pull request. |
| **Illustrative scenarios, clearly labelled** | Scenario numbers are financing anchors, not forecasts. |

---

## ⚡ Scope at a Glance

| Domain | Coverage | Key Output |
|--------|----------|------------|
| 🟢 **Green Bonds** | Sovereign, corporate & PSU issuance · 2015–present | Spread attribution vs. vanilla bonds; valuation model |
| 📊 **ESG Integration** | Nifty 50 + selected mid-cap universe | Weighted scoring model; sector benchmarks; data gap analysis |
| 🌡️ **Climate Risk** | Agriculture, power, infra, auto, cement | Portfolio Climate VaR; transition scenario stress tests |
| 🏛️ **SEBI / RBI Policy** | BRSR, green deposit frameworks, RBI circulars | Policy timeline; implementation gap analysis |
| ⚙️ **Transition Finance** | Cement, steel, coal power | Decarbonization capex DCF; SLB/transition bond structuring |
| 🏦 **Commercial Layer** | 9 India subsectors × 4 lifecycle stages | Deal economics, sector rankings, bank strategy plays |

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

**Key Finding:** No significant correlation between ESG score and returns in Indian equities yet — but sector bifurcation is pronounced: IT/pharma vs. metals/mining show a 70+ percentile gap on environmental scores.

---

## 🌡️ Climate Risk Modeling

Quantitative stress testing for physical and transition climate risks across Indian capital markets.

- Climate risk taxonomy: physical (rainfall, flooding, heat stress) vs. transition (carbon pricing, tech disruption)
- Portfolio Climate VaR under 1.5°C, 2°C, and delayed-transition scenarios
- India-specific scenario design: net-zero 2070 pathway, sectoral emissions caps

**Key Finding:** Under a 2°C transition scenario (carbon price ₹5,000/tonne by 2030), energy and materials sectors face 15–25% earnings headwinds.

---

## 🏛️ SEBI & RBI Policy

Timeline, implementation mechanics, and gap analysis of India's sustainable finance regulatory architecture.

- **SEBI BRSR Core** — mandatory for top 150 by market cap; third-party assured; vs. broader BRSR
- **RBI Climate Risk Circular** — principles-based guidance; enforcement timeline uncertainty
- Green deposit frameworks and ESG lending guidelines
- International alignment: TCFD, EU Taxonomy comparisons

**Key Finding:** SEBI's BRSR rollout is structurally comprehensive but enforcement is nascent. RBI guidance is principles-based, not rules-based — creating compliance ambiguity for regulated entities.

---

## ⚙️ Transition Finance

Structuring frameworks and financial models for decarbonisation of hard-to-abate sectors in India.

- **Cement** — fuel switching, clinker substitution, CCS readiness
- **Steel** — scrap-based EAF, hydrogen DRI transition economics
- **Coal Power** — plant retirement sequencing, refinancing gap modelling
- Capex requirement models, IRR sensitivity to carbon price

**Key Finding:** Cement sector decarbonisation cost is ₹8–12 per unit — viable within margin structure if carbon price exceeds ₹3,000/tonne.

---

## 🏦 Commercial Strategy Layer

A bank strategy engine that maps financing opportunities across 9 India subsectors and 4 lifecycle stages.

### What It Includes

| Module | Description |
|--------|-------------|
| `src/deal_economics.py` | Deal archetypes, annual volume, fee pool per subsector |
| `src/sector_priority.py` | Composite scoring model with configurable weights |
| `src/lifecycle.py` | Primary + secondary product per subsector × stage |
| `src/bank_strategy.py` | Capability-to-opportunity mapping; Lead/Co/Build plays |
| `src/commercial_report.py` | *Where the Money Is* — full strategy report |

### Instrument Taxonomy (9 Categories)

- Green project finance and corporate green loans
- Green bonds and green securitisation
- Sustainability-linked loans, RCFs, and bonds
- Transition finance loans and transition bond variants
- Warehouse and aggregation facilities
- Guarantees and partial risk-sharing facilities
- Blended finance and carbon-linked structures
- Advisory-led green / transition capital-markets mandates

### Bank Positioning

| Bank | Public Positioning | Source Basis |
|------|--------------------|-------------|
| **Standard Chartered** | EM-focused sustainable finance; explicit India transition strategy | Annual report, sustainability framework, India pages |
| **Deutsche Bank** | European anchor with growing EM transition coverage; ESG advisory depth | Sustainability report, product framework pages |
| **UBS** | Wealth-led sustainable investing; institutional green bond distribution | Annual report, sustainability report, press releases |

> All claims anchored to `data/bank_source_ledger.csv`. Unverified gaps labelled explicitly — never inferred.

---

## 🗂️ Repository Structure

```
sustainable-finance-india-transition/
│
├── 📁 .github/workflows/ci.yml          # GitHub Actions — test + rebuild on push
├── 📄 build.py                           # Single-command pipeline: reports + figures + CSVs
├── 📄 requirements.txt
├── 📁 config/
│   └── priority_weights.yaml             # Tunable sector scoring weights
├── 📁 data/
│   ├── green_bonds/                       # Issuance history, pricing spreads
│   ├── esg_scores/                        # Nifty 50 ESG metrics
│   ├── climate_scenarios/                 # Net-zero 2070 parameters
│   ├── deal_economics.csv                 # Commercial layer deal archetypes
│   ├── sector_capital_needs.csv           # Annual capital need by subsector
│   ├── bank_capabilities_template.csv     # Customisable bank profile
│   └── bank_source_ledger.csv             # Verified source references
├── 📁 src/
│   ├── taxonomy.py / scenarios.py / reporting.py   # Research layer
│   ├── portfolio_climate_var.py                     # Climate stress test
│   ├── sector_decarbonization_dcf.py                # Capex & IRR model
│   ├── esg_credit_spread_model.py                   # ESG spread attribution
│   ├── constants.py / deal_economics.py             # Commercial layer
│   ├── sector_priority.py / lifecycle.py            # Commercial layer
│   ├── bank_strategy.py / commercial_report.py      # Commercial layer
│   └── figures.py                                   # All chart generation
├── 📁 notebooks/                          # Jupyter demo workflows
├── 📁 reports/                            # Auto-generated outputs
└── 📁 tests/                              # pytest test suite
```

---

## 🚀 Quick Start

```bash
git clone https://github.com/DogInfantry/sustainable-finance-india-transition.git
cd sustainable-finance-india-transition
pip install -r requirements.txt
```

```python
# Research layer
from src.portfolio_climate_var import PortfolioClimateStress
results = PortfolioClimateStress(holdings, esg_ratings).stress_test(scenario='transition_2030')

from src.sector_decarbonization_dcf import SectorDCF
npv = SectorDCF(sector='cement', technology='clinker_substitution').run_valuation(capex_year=2025, carbon_price=5000)
```

```bash
# Commercial layer — regenerate all strategy outputs
python build.py

# Use your own bank profile
python build.py --bank-profile data/my_bank_capabilities.csv

# Run tests
pytest
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

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for setup instructions, branch naming convention, PR checklist, and data standards.

Quick labels to look for: `good first issue`, `data-gap`, `model-improvement`.

---

## ⚠️ Limitations

- **ESG data quality** — relies on company self-disclosure; cross-provider inconsistency is common
- **Scenario uncertainty** — climate pathways carry deep uncertainty; outputs are illustrative
- **Model sensitivity** — transition finance models are highly sensitive to capex profiles and carbon price assumptions
- **Deal economics** — all figures are illustrative estimates for strategic analysis; not market forecasts
- *Not investment advice. Not affiliated with Standard Chartered, Deutsche Bank, UBS, or any other institution.*

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

*Verified sources · Single-command reproducibility · Built for sustainable finance practitioners*

</div>
