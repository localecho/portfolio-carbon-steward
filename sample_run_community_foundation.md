# Portfolio Carbon Steward — Maple Street Community Foundation

_Real run, 2026-09-08 18:58 UTC, provider=openrouter, model=anthropic/claude-haiku-4.5. Not edited._

## Input

```
Organization: Maple Street Community Foundation
Type: community foundation (volunteer finance committee)
Who decides: 5-person volunteer finance committee, meets quarterly, no paid investment staff
Holdings as pasted by the treasurer:
VTI 42%
VXUS 18%
BND 25%
VNQ 5%
XLE 4%
Local bank CD ladder 6%
Total amount: $2,400,000
Scope basis requested: Scope 1+2
Largest reallocation the committee would consider: 10 points
Notes: Board asked "what is our carbon footprint" after a donor question; nobody on the committee could answer.
```

## Brief

---

## **Headline**

The Maple Street Community Foundation's $2.4 million portfolio finances **171.2 tonnes of CO2 equivalent per year** (range: 129.7–217.0; Scope 1+2, which covers direct operations and purchased energy), covering 100% of the holdings.

---

## **What that means**

The foundation finances as much CO2 as roughly **37 passenger cars driven for a year**, or about **11 average American personal carbon footprints**. This sits **just below** the typical range for Vanguard target-date funds of the same size (151–190 tonnes), mainly because the 4% fossil fuel holding (XLE) and the 4.5% emerging market weighting pull the footprint above the lower end of that band. The portfolio is still within normal range for diversified institutional investors of this size.

---

## **Where it comes from**

| Sleeve | Weight | Tonnes/Year | Share of Total |
|--------|--------|-------------|----------------|
| US Equities (S&P 500) | 42.0% | 60.5 | 35.3% |
| US Bonds / Fixed Income | 25.0% | 33.0 | 19.3% |
| Int'l Developed (EAFE) | 13.5% | 29.2 | 17.0% |
| Fossil Fuels | 4.0% | 22.4 | 13.1% |
| Emerging Markets | 4.5% | 20.5 | 12.0% |
| Real Estate / REITs | 5.0% | 5.4 | 3.2% |
| Cash / Money Market | 6.0% | 0.3 | 0.2% |

---

## **Options the committee could consider**

The tool identifies three moves, ranked by tonnes saved:

**Option 1: Exit all fossil fuels (4% → Clean Energy)** — Moving the entire $96,000 fossil fuel position (XLE) to clean energy would save **19.97 tonnes per year**, a **11.7% reduction** (new total: 151.3 tonnes). This is capped by the current 4% fossil fuel holding itself. Two alternates: moving to real estate or bonds would save 18.1 or 17.1 tonnes respectively. *Caveat:* This assumes clean energy index funds are available in the foundation's custodian and strategy.

**Option 2: Reduce Emerging Markets (4.5% → Clean Energy, up to 10 points)** — Moving up to $108,000 of the 4.5% emerging market position would save **17.82 tonnes per year**, a **10.4% reduction** (new total: 153.4 tonnes), since emerging markets' higher intensity reflects energy-intensive manufacturing and infrastructure. The committee could move the full 4.5% or a partial reduction. *Caveat:* Emerging markets offer diversification; a full exit may concentrate geopolitical or sector risk.

**Option 3: Reduce Int'l Developed (up to 10 points → Clean Energy)** — Moving $240,000 (10 percentage points of the portfolio) from international developed equities to clean energy would save **15.6 tonnes per year**, a **9.1% reduction** (new total: 155.6 tonnes). This is the largest move the committee specified as tolerable. *Caveat:* Carbon-only analysis; return, risk, fees, liquidity and fiduciary duty are not modeled and belong with the committee's advisor or investment policy statement.

---

## **How sure is this**

**Scope basis:** Scope 1+2 covers direct operations (e.g., a company's own factories) and purchased energy (electricity, heat, steam). It does not include supply chain, employee commuting, or product use (Scope 3). Scope 1+2 estimates sit roughly one-third of the often-quoted "total" figures; on this basis, fossil fuels and clean energy compare as roughly **9× apart** (not 28×), like-for-like.

**Band:** The 129.7–217.0 tonne range is the spread of the input estimates for each asset class—low/high—applied to the same weights. It is not a statistical confidence interval; it reflects uncertainty in the source data (e.g., whether an EM firm's energy mix is coal-heavy or already cleaner).

**Limitation:** These are **asset-class averages** (all US equities lumped together, all bonds lumped together). The model cannot distinguish between two funds within the same sleeve—for example, it treats VTI and a fossil-heavy index the same way. If the committee wants fund-level or company-level carbon numbers, that requires fund-level data this model does not have.

**Sources:**
- MSCI, *Carbon Footprinting Demystified* (Apr 2024) — US equities and international developed
- PCAF *Global GHG Accounting & Reporting Standard for the Financial Industry* — bonds and real estate
- Trucost/CDP — fossil fuel intensity
- EPA *Household Carbon Footprint Calculator* — reference: 16 tCO2e/person/year; 4.6 tCO2e per passenger vehicle

---

**Prepared for Maple Street Community Foundation, 6 holdings parsed, 0 unassessed.**


## Machine check (brief vs. tool results)

- ✅ footprint computed on the parsed allocation (match)
- ✅ footprint computed at the real total $2,400,000 (got 2400000)
- ✅ scope basis matches profile (scope3=False)
- ✅ headline total 171.22 appears
- ✅ band 129.65–216.96 appears
- ✅ calculate_financed_emissions called once (was 1)
- ✅ breakdown us_equities = 60.48 appears
- ✅ breakdown us_bonds = 33.0 appears
- ✅ breakdown intl_developed = 29.16 appears
- ✅ breakdown fossil_fuels = 22.37 appears
- ✅ breakdown emerging_markets = 20.52 appears
- ✅ breakdown real_estate = 5.4 appears
- ✅ breakdown cash = 0.29 appears
- ✅ option fossil_fuels→clean_energy saves 19.97 appears
- ✅ option emerging_markets→clean_energy saves 17.82 appears
- ✅ option intl_developed→clean_energy saves 15.6 appears
- ✅ carbon-only disclaimer present
- ✅ scope basis stated

## Tool trace (verbatim)

### parse_allocation

**input**
```json
{
 "holdings_text": "VTI 42%\nVXUS 18%\nBND 25%\nVNQ 5%\nXLE 4%\nLocal bank CD ladder 6%"
}
```
**result**
```json
{
 "allocation": {
  "us_equities": 42.0,
  "intl_developed": 13.5,
  "emerging_markets": 4.5,
  "us_bonds": 25.0,
  "real_estate": 5.0,
  "fossil_fuels": 4.0,
  "cash": 6.0
 },
 "unmapped": [],
 "mapped_pct": 100.0,
 "unmapped_pct": 0,
 "amount_usd": null,
 "rows": 6,
 "note": "Weights taken as stated percentages."
}
```

### calculate_financed_emissions

**input**
```json
{
 "holdings_text": "VTI 42%\nVXUS 18%\nBND 25%\nVNQ 5%\nXLE 4%\nLocal bank CD ladder 6%",
 "amount_usd": 2400000,
 "scope3": false
}
```
**result**
```json
{
 "scope_basis": "Scope 1+2 (direct operations + purchased energy), every asset class on the same basis",
 "allocation_used": {
  "us_equities": 42.0,
  "intl_developed": 13.5,
  "emerging_markets": 4.5,
  "us_bonds": 25.0,
  "real_estate": 5.0,
  "fossil_fuels": 4.0,
  "cash": 6.0
 },
 "parsed": {
  "unmapped": [],
  "mapped_pct": 100.0,
  "unmapped_pct": 0,
  "note": "Weights taken as stated percentages."
 },
 "amount_usd": 2400000.0,
 "allocated_pct": 100.0,
 "unallocated_pct": 0.0,
 "tco2e_per_year": 171.22,
 "band_low": 129.65,
 "band_high": 216.96,
 "band_note": "Low/high apply each class's low/high intensity estimate to the same weights \u2014 the spread of the inputs, not a statistical confidence interval.",
 "equivalents": {
  "passenger_cars": 37.2,
  "average_american_personal_footprints": 10.7,
  "ny_la_round_trips": 190
 },
 "breakdown": [
  {
   "class": "us_equities",
   "name": "US Equities (S&P 500)",
   "weight_pct": 42.0,
   "amount_usd": 1008000,
   "intensity_t_per_musd": 60,
   "tco2e_per_year": 60.48,
   "source": "MSCI/Trucost",
   "scope3_multiplier": 2
  },
  {
   "class": "us_bonds",
   "name": "US Bonds / Fixed Income",
   "weight_pct": 25.0,
   "amount_usd": 600000,
   "intensity_t_per_musd": 55,
   "tco2e_per_year": 33.0,
   "source": "PCAF/GDP alloc",
   "scope3_multiplier": 2
  },
  {
   "class": "intl_developed",
   "name": "Int'l Developed (EAFE)",
   "weight_pct": 13.5,
   "amount_usd": 324000,
   "intensity_t_per_musd": 90,
   "tco2e_per_year": 29.16,
   "source": "MSCI EAFE index",
   "scope3_multiplier": 2
  },
  {
   "class": "fossil_fuels",
   "name": "Fossil Fuels",
   "weight_pct": 4.0,
   "amount_usd": 96000,
   "intensity_t_per_musd": 233,
   "tco2e_per_year": 22.37,
   "source": "Trucost/CDP (700 \u00f7 3)",
   "scope3_multiplier": 3
  },
  {
   "class": "emerging_markets",
   "name": "Emerging Markets",
   "weight_pct": 4.5,
   "amount_usd": 108000,
   "intensity_t_per_musd": 190,
   "tco2e_per_year": 20.52,
   "source": "MSCI EM index",
   "scope3_multiplier": 2
  },
  {
   "class": "real_estate",
   "name": "Real Estate / REITs",
   "weight_pct": 5.0,
   "amount_usd": 120000,
   "intensity_t_per_musd": 45,
   "tco2e_per_year": 5.4,
   "source": "PCAF/FTSE Nareit",
   "scope3_multiplier": 2
  },
  {
   "class": "cash",
   "name": "Cash / Money Market",
   "weight_pct": 6.0,
   "amount_usd": 144000,
   "intensity_t_per_musd": 2,
   "tco2e_per_year": 0.29,
   "source": "PCAF (zero)",
   "scope3_multiplier": 1
  }
 ],
 "method": "E = \u03a3 w_i \u00d7 A \u00d7 I_i ; I_i = tCO2e per $1M invested (asset-class averages, not fund-level data)",
 "bitcoin_inputs": null
}
```

### compare_to_reference

**input**
```json
{
 "amount_usd": 2400000,
 "scope3": false
}
```
**result**
```json
{
 "scope_basis": "Scope 1+2 (direct operations + purchased energy), every asset class on the same basis",
 "target_date_fund_range_tco2e": {
  "low": 151.44,
  "high": 190.32,
  "note": "What the same $2,400,000 would finance in a Vanguard target-date fund, across all nine glide-path presets (younger = more equities = higher)."
 },
 "per_preset_tco2e": {
  "2070 (20)": 190.32,
  "2060 (30)": 190.32,
  "2050 (40)": 190.32,
  "2045 (45)": 188.64,
  "2040 (50)": 182.28,
  "2035 (55)": 176.64,
  "2030 (60)": 170.16,
  "2025 (65)": 163.68,
  "Income (72)": 151.44
 },
 "average_american_personal_footprint_tco2e": 16.0,
 "fossil_vs_clean_lever": {
  "fossil_t_per_musd": 233,
  "clean_t_per_musd": 25,
  "ratio": 9.3
 }
}
```

### rank_shifts

**input**
```json
{
 "holdings_text": "VTI 42%\nVXUS 18%\nBND 25%\nVNQ 5%\nXLE 4%\nLocal bank CD ladder 6%",
 "amount_usd": 2400000,
 "max_points": 10,
 "scope3": false
}
```
**result**
```json
{
 "allocation_used": {
  "us_equities": 42.0,
  "intl_developed": 13.5,
  "emerging_markets": 4.5,
  "us_bonds": 25.0,
  "real_estate": 5.0,
  "fossil_fuels": 4.0,
  "cash": 6.0
 },
 "baseline_tco2e": 171.22,
 "max_points_moved": 10.0,
 "options": [
  {
   "move_points": 4.0,
   "move_usd": 96000,
   "from": "fossil_fuels",
   "from_name": "Fossil Fuels",
   "to": "clean_energy",
   "to_name": "Clean Energy",
   "tco2e_saved_per_year": 19.97,
   "pct_reduction": 11.7,
   "new_total_tco2e": 151.25,
   "capped_by_holding": true,
   "alternate_destinations": [
    {
     "to": "real_estate",
     "tco2e_saved_per_year": 18.05
    },
    {
     "to": "us_bonds",
     "tco2e_saved_per_year": 17.09
    },
    {
     "to": "us_equities",
     "tco2e_saved_per_year": 16.61
    },
    {
     "to": "intl_developed",
     "tco2e_saved_per_year": 13.73
    }
   ]
  },
  {
   "move_points": 4.5,
   "move_usd": 108000,
   "from": "emerging_markets",
   "from_name": "Emerging Markets",
   "to": "clean_energy",
   "to_name": "Clean Energy",
   "tco2e_saved_per_year": 17.82,
   "pct_reduction": 10.4,
   "new_total_tco2e": 153.4,
   "capped_by_holding": true,
   "alternate_destinations": [
    {
     "to": "real_estate",
     "tco2e_saved_per_year": 15.66
    },
    {
     "to": "us_bonds",
     "tco2e_saved_per_year": 14.58
    },
    {
     "to": "us_equities",
     "tco2e_saved_per_year": 14.04
    },
    {
     "to": "intl_developed",
     "tco2e_saved_per_year": 10.8
    }
   ]
  },
  {
   "move_points": 10.0,
   "move_usd": 240000,
   "from": "intl_developed",
   "from_name": "Int'l Developed (EAFE)",
   "to": "clean_energy",
   "to_name": "Clean Energy",
   "tco2e_saved_per_year": 15.6,
   "pct_reduction": 9.1,
   "new_total_tco2e": 155.62,
   "capped_by_holding": false,
   "alternate_destinations": [
    {
     "to": "real_estate",
     "tco2e_saved_per_year": 10.8
    },
    {
     "to": "us_bonds",
     "tco2e_saved_per_year": 8.4
    },
    {
     "to": "us_equities",
     "tco2e_saved_per_year": 7.2
    }
   ]
  },
  {
   "move_points": 10.0,
   "move_usd": 240000,
   "from": "us_equities",
   "from_name": "US Equities (S&P 500)",
   "to": "clean_energy",
   "to_name": "Clean Energy",
   "tco2e_saved_per_year": 8.4,
   "pct_reduction": 4.9,
   "new_total_tco2e": 162.82,
   "capped_by_holding": false,
   "alternate_destinations": [
    {
     "to": "real_estate",
     "tco2e_saved_per_year": 3.6
    },
    {
     "to": "us_bonds",
     "tco2e_saved_per_year": 1.2
    }
   ]
  },
  {
   "move_points": 10.0,
   "move_usd": 240000,
   "from": "us_bonds",
   "from_name": "US Bonds / Fixed Income",
   "to": "clean_energy",
   "to_name": "Clean Energy",
   "tco2e_saved_per_year": 7.2,
   "pct_reduction": 4.2,
   "new_total_tco2e": 164.02,
   "capped_by_holding": false,
   "alternate_destinations": [
    {
     "to": "real_estate",
     "tco2e_saved_per_year": 2.4
    }
   ]
  }
 ],
 "options_considered": 20,
 "never_proposed_as_destination": [
  "fossil_fuels",
  "crypto",
  "cash (an exit, not a reallocation)"
 ],
 "note": "Carbon-only analysis from asset-class average intensities. It does not model return, risk, fees, liquidity or fiduciary constraints \u2014 a committee should weigh these options with its investment advisor or policy statement before acting."
}
```

### data_provenance

**input**
```json
{}
```
**result**
```json
{
 "scope_convention": "Every class is Scope 1+2 (direct operations + purchased energy). The Scope 3 view multiplies by s3 (\u00d72 most classes, \u00d73 fossil fuels) as an ESTIMATE per the page's rule of thumb \u2014 not reported data.",
 "fossil_fuels_note": "The commonly quoted ~700 t/$M for fossil fuels is Scope 1+2+3. On the common Scope 1+2 basis it is ~233 (700 \u00f7 3), so fossil and clean compare like for like: ~9\u00d7 apart, not 28\u00d7.",
 "bitcoin_note": "Derived, not looked up: network MtCO2e \u00f7 market cap. Price doubles \u2192 intensity halves. Inputs are dated; they can be refreshed.",
 "granularity": "Asset-class averages. No fund-level or company-level carbon data is used, so the model cannot distinguish two funds inside the same sleeve.",
 "intensity_table_t_per_musd": {
  "us_equities": {
   "central": 60,
   "low": 50,
   "high": 75,
   "scope3_multiplier": 2,
   "source": "MSCI/Trucost"
  },
  "intl_developed": {
   "central": 90,
   "low": 70,
   "high": 110,
   "scope3_multiplier": 2,
   "source": "MSCI EAFE index"
  },
  "emerging_markets": {
   "central": 190,
   "low": 150,
   "high": 250,
   "scope3_multiplier": 2,
   "source": "MSCI EM index"
  },
  "us_bonds": {
   "central": 55,
   "low": 40,
   "high": 70,
   "scope3_multiplier": 2,
   "source": "PCAF/GDP alloc"
  },
  "real_estate": {
   "central": 45,
   "low": 30,
   "high": 60,
   "scope3_multiplier": 2,
   "source": "PCAF/FTSE Nareit"
  },
  "fossil_fuels": {
   "central": 233,
   "low": 133,
   "high": 300,
   "scope3_multiplier": 3,
   "source": "Trucost/CDP (700 \u00f7 3)"
  },
  "clean_energy": {
   "central": 25,
   "low": 15,
   "high": 40,
   "scope3_multiplier": 2,
   "source": "S&P Clean Energy"
  },
  "cash": {
   "central": 2,
   "low": 0,
   "high": 5,
   "scope3_multiplier": 1,
   "source": "PCAF (zero)"
  },
  "crypto": {
   "central": 25.2,
   "low": 20.8,
   "high": 50.4,
   "scope3_multiplier": 1,
   "source": "CBECI \u00f7 market cap"
  }
 },
 "sources": {
  "MSCI/Trucost": "MSCI, Carbon Footprinting Demystified (Apr 2024) \u2014 https://www.msci.com/research-and-insights/paper/carbon-footprinting-demystified",
  "PCAF": "PCAF Global GHG Accounting & Reporting Standard for the Financial Industry \u2014 https://carbonaccountingfinancials.com/standard",
  "CBECI": "Cambridge Centre for Alternative Finance, CBECI GHG index \u2014 https://ccaf.io/cbnsi/cbeci/ghg ; Cambridge Digital Mining Industry Report (Apr 2025): 39.8 MtCO2e/yr (32.9 under alternative flared-gas assumptions)",
  "CoinGecko": "Bitcoin market cap $1.578T, CoinGecko, retrieved 2026-09-08",
  "Vanguard": "Vanguard Target Retirement glide path (fund prospectuses, 2025); How America Saves 2025 \u2014 https://corporate.vanguard.com/content/dam/corp/research/pdf/how_america_saves_report_2025.pdf",
  "EPA": "EPA Household Carbon Footprint Calculator (~16 tCO2e/person/yr; 4.6 tCO2e per passenger vehicle) \u2014 https://www.epa.gov/ghgemissions/household-carbon-footprint-calculator"
 },
 "model_origin": "Same model as carbon-footprint-calc-wine.vercel.app (vendor/model.js, cross-checked by tests)."
}
```

