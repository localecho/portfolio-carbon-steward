# Portfolio Carbon Steward — Lincoln Elementary PTA Reserve Fund

_Real run, 2026-09-08 19:00 UTC, provider=openrouter, model=anthropic/claude-haiku-4.5. Not edited._

## Input

```
Organization: Lincoln Elementary PTA Reserve Fund
Type: PTA reserve fund
Who decides: PTA treasurer + 3 officers, annual vote
Holdings as pasted by the treasurer:
$38,000 in a Fidelity money market (SPAXX)
$52,000 in FXAIX
$10,000 in a school-district credit union savings account
Scope basis requested: Scope 1+2
Largest reallocation the committee would consider: 15 points
Notes: Statement pasted in dollars; total should be derived by the agent.
```

## Brief

---

## **Headline**

The Lincoln Elementary PTA Reserve Fund finances **3.22 tonnes of CO₂e per year** (low–high: 2.6–4.14) on a Scope 1+2 basis, across all **$100,000** of holdings.

---

## **What that means**

This is equivalent to **0.7 passenger cars** driven for a year, or about **1/5 of one average American's personal footprint** (16 tCO2e/yr). Compared to Vanguard's target-date funds at the same dollar amount, the PTA's footprint falls well below the range (6.31–7.93 tCO2e), meaning the fund is financed less carbon-intensive companies and sectors on average.

---

## **Where it comes from**

| Sleeve | Weight | Tonnes/yr | Share |
|--------|--------|-----------|-------|
| US Equities (S&P 500) | 52% | 3.12 | 97% |
| Cash / Money Market | 48% | 0.1 | 3% |
| **Total** | **100%** | **3.22** | **100%** |

---

## **Options the committee could consider**

1. **Move 15 percentage points ($15,000) from US Equities into Clean Energy.**  
   Tonnes saved: 0.53 per year. Reduction: 16.3%, bringing the total to 2.69 tCO2e/yr.  
   *Note:* Clean energy funds concentrate in a smaller sector; diversification and returns depend on your advisor's assessment.

2. **Move 15 percentage points ($15,000) from US Equities into Real Estate.**  
   Tonnes saved: 0.22 per year. Reduction: 6.8%, bringing the total to 3.00 tCO2e/yr.  
   *Note:* Real estate adds exposure to real-asset inflation hedge but shifts sector exposure.

3. **Move 15 percentage points ($15,000) from US Equities into US Bonds.**  
   Tonnes saved: 0.07 per year. Reduction: 2.1%, bringing the total to 3.15 tCO2e/yr.  
   *Note:* Bonds typically lower portfolio volatility but offer lower long-term equity returns.

**Carbon-only disclaimer:** These options rank by tonnes saved annually and do not model return, risk, fees, liquidity, or fiduciary duty — all of which belong with your investment advisor or the PTA's investment policy statement before any move is made.

---

## **How sure is this**

**Scope basis:** Scope 1+2 (direct operations and purchased energy) — all asset classes on the same basis. The band (2.6–4.14 tCO2e) reflects the range of low and high intensity estimates for each class using the same weights; it is the spread of the inputs, not a statistical confidence interval.

**Asset-class averages:** This model uses average carbon intensity for each investment sleeve (US equities, cash, etc.) and cannot distinguish the carbon footprint of one fund from another inside the same class. For fund-level or company-level carbon data, your advisor would need to source that separately.

**Sources:**
- **MSCI/Trucost** (Apr 2024): US equities intensity of 60 tCO2e per $1M invested — https://www.msci.com/research-and-insights/paper/carbon-footprinting-demystified
- **PCAF** Global GHG Accounting & Reporting Standard: Cash/money market, SPAXX, and bond intensities — https://carbonaccountingfinancials.com/standard
- **EPA** Household Carbon Footprint Calculator: Average American baseline (~16 tCO2e/person/yr) — https://www.epa.gov/ghgemissions/household-carbon-footprint-calculator

---

Prepared for Lincoln Elementary PTA Reserve Fund, 3 holdings parsed, 0 unassessed.


## Machine check (brief vs. tool results)

- ✅ footprint computed on the parsed allocation (match)
- ✅ footprint computed at the real total $100,000 (got 100000.0)
- ✅ scope basis matches profile (scope3=False)
- ✅ headline total 3.22 appears
- ✅ band 2.6–4.14 appears
- ✅ calculate_financed_emissions called once (was 1)
- ✅ breakdown us_equities = 3.12 appears
- ✅ breakdown cash = 0.1 appears
- ✅ option us_equities→clean_energy saves 0.53 appears
- ✅ carbon-only disclaimer present
- ✅ scope basis stated

## Tool trace (verbatim)

### parse_allocation

**input**
```json
{
 "holdings_text": "$38,000 in a Fidelity money market (SPAXX)\n$52,000 in FXAIX\n$10,000 in a school-district credit union savings account"
}
```
**result**
```json
{
 "allocation": {
  "cash": 48.0,
  "us_equities": 52.0
 },
 "unmapped": [],
 "mapped_pct": 100.0,
 "unmapped_pct": 0,
 "amount_usd": 100000.0,
 "rows": 3,
 "note": "Weights derived from dollar amounts."
}
```

### calculate_financed_emissions

**input**
```json
{
 "holdings_text": "$38,000 in a Fidelity money market (SPAXX)\n$52,000 in FXAIX\n$10,000 in a school-district credit union savings account",
 "scope3": false
}
```
**result**
```json
{
 "scope_basis": "Scope 1+2 (direct operations + purchased energy), every asset class on the same basis",
 "allocation_used": {
  "cash": 48.0,
  "us_equities": 52.0
 },
 "parsed": {
  "unmapped": [],
  "mapped_pct": 100.0,
  "unmapped_pct": 0,
  "note": "Weights derived from dollar amounts."
 },
 "amount_usd": 100000.0,
 "allocated_pct": 100.0,
 "unallocated_pct": 0.0,
 "tco2e_per_year": 3.22,
 "band_low": 2.6,
 "band_high": 4.14,
 "band_note": "Low/high apply each class's low/high intensity estimate to the same weights \u2014 the spread of the inputs, not a statistical confidence interval.",
 "equivalents": {
  "passenger_cars": 0.7,
  "average_american_personal_footprints": 0.2,
  "ny_la_round_trips": 4
 },
 "breakdown": [
  {
   "class": "us_equities",
   "name": "US Equities (S&P 500)",
   "weight_pct": 52.0,
   "amount_usd": 52000,
   "intensity_t_per_musd": 60,
   "tco2e_per_year": 3.12,
   "source": "MSCI/Trucost",
   "scope3_multiplier": 2
  },
  {
   "class": "cash",
   "name": "Cash / Money Market",
   "weight_pct": 48.0,
   "amount_usd": 48000,
   "intensity_t_per_musd": 2,
   "tco2e_per_year": 0.1,
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
 "amount_usd": 100000,
 "scope3": false
}
```
**result**
```json
{
 "scope_basis": "Scope 1+2 (direct operations + purchased energy), every asset class on the same basis",
 "target_date_fund_range_tco2e": {
  "low": 6.31,
  "high": 7.93,
  "note": "What the same $100,000 would finance in a Vanguard target-date fund, across all nine glide-path presets (younger = more equities = higher)."
 },
 "per_preset_tco2e": {
  "2070 (20)": 7.93,
  "2060 (30)": 7.93,
  "2050 (40)": 7.93,
  "2045 (45)": 7.86,
  "2040 (50)": 7.59,
  "2035 (55)": 7.36,
  "2030 (60)": 7.09,
  "2025 (65)": 6.82,
  "Income (72)": 6.31
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
 "holdings_text": "$38,000 in a Fidelity money market (SPAXX)\n$52,000 in FXAIX\n$10,000 in a school-district credit union savings account",
 "max_points": 15,
 "scope3": false
}
```
**result**
```json
{
 "allocation_used": {
  "cash": 48.0,
  "us_equities": 52.0
 },
 "baseline_tco2e": 3.22,
 "max_points_moved": 15.0,
 "options": [
  {
   "move_points": 15.0,
   "move_usd": 15000,
   "from": "us_equities",
   "from_name": "US Equities (S&P 500)",
   "to": "clean_energy",
   "to_name": "Clean Energy",
   "tco2e_saved_per_year": 0.53,
   "pct_reduction": 16.3,
   "new_total_tco2e": 2.69,
   "capped_by_holding": false,
   "alternate_destinations": [
    {
     "to": "real_estate",
     "tco2e_saved_per_year": 0.22
    },
    {
     "to": "us_bonds",
     "tco2e_saved_per_year": 0.07
    }
   ]
  }
 ],
 "options_considered": 3,
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

