# Portfolio Carbon Steward — First Congregational Endowment Committee

_Real run, 2026-09-08 18:58 UTC, provider=openrouter, model=anthropic/claude-haiku-4.5. Not edited._

## Input

```
Organization: First Congregational Endowment Committee
Type: congregation endowment
Who decides: endowment committee of 7, meets twice a year
Holdings as pasted by the treasurer:
55% US stock index fund
20% international stock fund
20% bond fund
3% Bitcoin ETF (IBIT) a member donated
2% "Legacy Growth Fund" (details unknown)
Total amount: $1,150,000
Scope basis requested: Scope 1+2 + estimated Scope 3
Largest reallocation the committee would consider: 10 points
Notes: Committee wants to see the Scope 3 view because a member read about it. One holding is unidentifiable.
```

## Brief

---

## **Financed Emissions Brief: First Congregational Endowment Committee**

### **Headline**

The endowment finances **154.97 tonnes of CO₂ equivalent per year** (range 123.77–195.52, Scope 1+2 plus estimated Scope 3), on the $1,150,000 currently mapped—covering 98% of the portfolio; 2% of holdings could not be identified.

### **What that means**

This is equivalent to:
- Driving **33.7 passenger cars** for a year
- The personal carbon footprint of **9.7 average Americans**
- Flying between New York and Los Angeles **172 times**

The endowment's footprint sits **within the range** of a typical Vanguard target-date fund at the same size (145–182 tonnes/year). It exceeds an average American's personal footprint of 16 tonnes/year by roughly 10×, reflecting the leverage effect of invested capital financing companies' operations rather than direct personal emissions.

### **Where it comes from**

| Sleeve | Weight | Tonnes/year | Share of total |
|--------|--------|-------------|----------------|
| US Equities (S&P 500) | 55% | 75.9 | 49.0% |
| Int'l Developed (EAFE) | 15% | 31.05 | 20.0% |
| Emerging Markets | 5% | 21.85 | 14.1% |
| US Bonds / Fixed Income | 20% | 25.3 | 16.3% |
| Crypto / Bitcoin | 3% | 0.87 | 0.6% |

### **Unassessed**

- "Legacy Growth Fund" (details unknown): **2%** of portfolio

This holding carries no carbon estimate because it could not be mapped to an asset class. The committee should ask the donor or the fund custodian for the holdings inside it so a full footprint can be calculated.

### **Options the committee could consider**

1. **Move 5 percentage points ($57,500) from Emerging Markets into Clean Energy**  
   Saves **18.97 tonnes/year** → **12.2% reduction** → new total 136.0 tonnes/year.  
   *Caveat:* This move exhausts the entire Emerging Markets holding; the committee must decide if international diversification is acceptable to sacrifice entirely or if a smaller shift makes more sense.  
   **Carbon-only analysis.** Return, risk, fees, liquidity and fiduciary duty are not modeled and belong with the committee's advisor or investment policy statement.

2. **Move 10 percentage points ($115,000) from Int'l Developed (EAFE) into Clean Energy**  
   Saves **14.95 tonnes/year** → **9.6% reduction** → new total 140.02 tonnes/year.  
   *Caveat:* This reduces international exposure by one-third while maintaining diversification across the larger sleeves.

3. **Move 10 percentage points ($115,000) from US Equities into Clean Energy**  
   Saves **8.05 tonnes/year** → **5.2% reduction** → new total 146.92 tonnes/year.  
   *Caveat:* This is the largest holding; the impact is smaller per point because US equities already have lower carbon intensity than emerging markets.

### **How sure is this**

**Scope basis:** Scope 1+2 (direct operations and purchased energy) plus an estimated Scope 3 uplift (×2 for most classes, ×3 for fossil fuels) as a rule of thumb—not reported data.

**Band:** 123.77–195.52 tonnes/year. This reflects the spread of low and high intensity estimates across all five asset classes, not a statistical confidence interval. The true figure depends on which funds inside each sleeve the committee actually holds.

**Asset-class averages:** These are class-level figures, not fund-specific data. Two different "US stock index funds" may have different holdings; the model cannot distinguish them. For fund-level carbon figures, request prospectuses or third-party carbon ratings from your investment custodian.

**Bitcoin inputs (IBIT):** The intensity of 25.2 tCO2e/$M is derived from network emissions (39.8 MtCO2e/year per the Cambridge Centre for Alternative Finance, as of 2026-09-08) divided by market cap ($1.578T). If the Bitcoin price moves, the intensity per dollar moves inversely; these inputs can be refreshed.

**Sources:**
- MSCI, *Carbon Footprinting Demystified* (Apr 2024) — US and Emerging Markets equities
- PCAF, *Global GHG Accounting & Reporting Standard for the Financial Industry* — bonds
- Cambridge Centre for Alternative Finance, CBECI GHG index — Bitcoin
- EPA, *Household Carbon Footprint Calculator* — personal footprint equivalents

---

**Prepared for First Congregational Endowment Committee, 5 holdings parsed, 1 unassessed.**


## Machine check (brief vs. tool results)

- ✅ footprint computed on the parsed allocation (match)
- ✅ footprint computed at the real total $1,150,000 (got 1150000)
- ✅ scope basis matches profile (scope3=True)
- ✅ headline total 154.97 appears
- ✅ band 123.77–195.52 appears
- ✅ calculate_financed_emissions called once (was 1)
- ✅ breakdown us_equities = 75.9 appears
- ✅ breakdown intl_developed = 31.05 appears
- ✅ breakdown us_bonds = 25.3 appears
- ✅ breakdown emerging_markets = 21.85 appears
- ✅ breakdown crypto = 0.87 appears
- ✅ option emerging_markets→clean_energy saves 18.97 appears
- ✅ option intl_developed→clean_energy saves 14.95 appears
- ✅ option us_equities→clean_energy saves 8.05 appears
- ✅ unassessed section present for unmapped holdings
- ✅ carbon-only disclaimer present
- ✅ scope basis stated

## Tool trace (verbatim)

### parse_allocation

**input**
```json
{
 "holdings_text": "55% US stock index fund\n20% international stock fund\n20% bond fund\n3% Bitcoin ETF (IBIT) a member donated\n2% \"Legacy Growth Fund\" (details unknown)"
}
```
**result**
```json
{
 "allocation": {
  "us_equities": 55.0,
  "intl_developed": 15.0,
  "emerging_markets": 5.0,
  "us_bonds": 20.0,
  "crypto": 3.0
 },
 "unmapped": [
  {
   "holding": "2% \"Legacy Growth Fund\" (details unknown)",
   "pct": 2.0
  }
 ],
 "mapped_pct": 98.0,
 "unmapped_pct": 2.0,
 "amount_usd": null,
 "rows": 5,
 "note": "Weights taken as stated percentages. Unmapped holdings carry NO carbon estimate and must be reported as unassessed."
}
```

### calculate_financed_emissions

**input**
```json
{
 "holdings_text": "55% US stock index fund\n20% international stock fund\n20% bond fund\n3% Bitcoin ETF (IBIT) a member donated\n2% \"Legacy Growth Fund\" (details unknown)",
 "amount_usd": 1150000,
 "scope3": true
}
```
**result**
```json
{
 "scope_basis": "Scope 1+2 plus an ESTIMATED Scope 3 uplift (\u00d72 most classes, \u00d73 fossil fuels)",
 "allocation_used": {
  "us_equities": 55.0,
  "intl_developed": 15.0,
  "emerging_markets": 5.0,
  "us_bonds": 20.0,
  "crypto": 3.0
 },
 "parsed": {
  "unmapped": [
   {
    "holding": "2% \"Legacy Growth Fund\" (details unknown)",
    "pct": 2.0
   }
  ],
  "mapped_pct": 98.0,
  "unmapped_pct": 2.0,
  "note": "Weights taken as stated percentages. Unmapped holdings carry NO carbon estimate and must be reported as unassessed."
 },
 "amount_usd": 1150000.0,
 "allocated_pct": 98.0,
 "unallocated_pct": 2.0,
 "tco2e_per_year": 154.97,
 "band_low": 123.77,
 "band_high": 195.52,
 "band_note": "Low/high apply each class's low/high intensity estimate to the same weights \u2014 the spread of the inputs, not a statistical confidence interval.",
 "equivalents": {
  "passenger_cars": 33.7,
  "average_american_personal_footprints": 9.69,
  "ny_la_round_trips": 172
 },
 "breakdown": [
  {
   "class": "us_equities",
   "name": "US Equities (S&P 500)",
   "weight_pct": 55.0,
   "amount_usd": 632500,
   "intensity_t_per_musd": 120,
   "tco2e_per_year": 75.9,
   "source": "MSCI/Trucost",
   "scope3_multiplier": 2
  },
  {
   "class": "intl_developed",
   "name": "Int'l Developed (EAFE)",
   "weight_pct": 15.0,
   "amount_usd": 172500,
   "intensity_t_per_musd": 180,
   "tco2e_per_year": 31.05,
   "source": "MSCI EAFE index",
   "scope3_multiplier": 2
  },
  {
   "class": "us_bonds",
   "name": "US Bonds / Fixed Income",
   "weight_pct": 20.0,
   "amount_usd": 230000,
   "intensity_t_per_musd": 110,
   "tco2e_per_year": 25.3,
   "source": "PCAF/GDP alloc",
   "scope3_multiplier": 2
  },
  {
   "class": "emerging_markets",
   "name": "Emerging Markets",
   "weight_pct": 5.0,
   "amount_usd": 57500,
   "intensity_t_per_musd": 380,
   "tco2e_per_year": 21.85,
   "source": "MSCI EM index",
   "scope3_multiplier": 2
  },
  {
   "class": "crypto",
   "name": "Crypto / Bitcoin",
   "weight_pct": 3.0,
   "amount_usd": 34500,
   "intensity_t_per_musd": 25.2,
   "tco2e_per_year": 0.87,
   "source": "CBECI \u00f7 market cap",
   "scope3_multiplier": 1
  }
 ],
 "method": "E = \u03a3 w_i \u00d7 A \u00d7 I_i ; I_i = tCO2e per $1M invested (asset-class averages, not fund-level data)",
 "bitcoin_inputs": {
  "mt_per_year": 39.8,
  "market_cap_usd": 1578000000000.0,
  "as_of": "2026-09-08"
 }
}
```

### compare_to_reference

**input**
```json
{
 "amount_usd": 1150000,
 "scope3": true
}
```
**result**
```json
{
 "scope_basis": "Scope 1+2 plus an ESTIMATED Scope 3 uplift (\u00d72 most classes, \u00d73 fossil fuels)",
 "target_date_fund_range_tco2e": {
  "low": 145.13,
  "high": 182.39,
  "note": "What the same $1,150,000 would finance in a Vanguard target-date fund, across all nine glide-path presets (younger = more equities = higher)."
 },
 "per_preset_tco2e": {
  "2070 (20)": 182.39,
  "2060 (30)": 182.39,
  "2050 (40)": 182.39,
  "2045 (45)": 180.78,
  "2040 (50)": 174.69,
  "2035 (55)": 169.28,
  "2030 (60)": 163.07,
  "2025 (65)": 156.86,
  "Income (72)": 145.13
 },
 "average_american_personal_footprint_tco2e": 16.0,
 "fossil_vs_clean_lever": {
  "fossil_t_per_musd": 699,
  "clean_t_per_musd": 50,
  "ratio": 14.0
 }
}
```

### rank_shifts

**input**
```json
{
 "holdings_text": "55% US stock index fund\n20% international stock fund\n20% bond fund\n3% Bitcoin ETF (IBIT) a member donated\n2% \"Legacy Growth Fund\" (details unknown)",
 "amount_usd": 1150000,
 "max_points": 10,
 "scope3": true
}
```
**result**
```json
{
 "allocation_used": {
  "us_equities": 55.0,
  "intl_developed": 15.0,
  "emerging_markets": 5.0,
  "us_bonds": 20.0,
  "crypto": 3.0
 },
 "baseline_tco2e": 154.97,
 "max_points_moved": 10.0,
 "options": [
  {
   "move_points": 5.0,
   "move_usd": 57500,
   "from": "emerging_markets",
   "from_name": "Emerging Markets",
   "to": "clean_energy",
   "to_name": "Clean Energy",
   "tco2e_saved_per_year": 18.97,
   "pct_reduction": 12.2,
   "new_total_tco2e": 136.0,
   "capped_by_holding": true,
   "alternate_destinations": [
    {
     "to": "real_estate",
     "tco2e_saved_per_year": 16.67
    },
    {
     "to": "us_bonds",
     "tco2e_saved_per_year": 15.52
    },
    {
     "to": "us_equities",
     "tco2e_saved_per_year": 14.95
    },
    {
     "to": "intl_developed",
     "tco2e_saved_per_year": 11.5
    }
   ]
  },
  {
   "move_points": 10.0,
   "move_usd": 115000,
   "from": "intl_developed",
   "from_name": "Int'l Developed (EAFE)",
   "to": "clean_energy",
   "to_name": "Clean Energy",
   "tco2e_saved_per_year": 14.95,
   "pct_reduction": 9.6,
   "new_total_tco2e": 140.02,
   "capped_by_holding": false,
   "alternate_destinations": [
    {
     "to": "real_estate",
     "tco2e_saved_per_year": 10.35
    },
    {
     "to": "us_bonds",
     "tco2e_saved_per_year": 8.05
    },
    {
     "to": "us_equities",
     "tco2e_saved_per_year": 6.9
    }
   ]
  },
  {
   "move_points": 10.0,
   "move_usd": 115000,
   "from": "us_equities",
   "from_name": "US Equities (S&P 500)",
   "to": "clean_energy",
   "to_name": "Clean Energy",
   "tco2e_saved_per_year": 8.05,
   "pct_reduction": 5.2,
   "new_total_tco2e": 146.92,
   "capped_by_holding": false,
   "alternate_destinations": [
    {
     "to": "real_estate",
     "tco2e_saved_per_year": 3.45
    },
    {
     "to": "us_bonds",
     "tco2e_saved_per_year": 1.15
    }
   ]
  },
  {
   "move_points": 10.0,
   "move_usd": 115000,
   "from": "us_bonds",
   "from_name": "US Bonds / Fixed Income",
   "to": "clean_energy",
   "to_name": "Clean Energy",
   "tco2e_saved_per_year": 6.9,
   "pct_reduction": 4.5,
   "new_total_tco2e": 148.07,
   "capped_by_holding": false,
   "alternate_destinations": [
    {
     "to": "real_estate",
     "tco2e_saved_per_year": 2.3
    }
   ]
  }
 ],
 "options_considered": 14,
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

