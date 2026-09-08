# Portfolio Carbon Steward — Northside Co-op 401(k) Committee

_Real run, 2026-09-08 18:59 UTC, provider=openrouter, model=anthropic/claude-haiku-4.5. Not edited._

## Input

```
Organization: Northside Co-op 401(k) Committee
Type: employer 401(k) plan committee
Who decides: 4-person plan committee choosing the default fund lineup for 60 employees
Calculator share link: https://carbon-footprint-calc-wine.vercel.app/#a=us_%3A54%2Cint%3A27%2Ceme%3A9%2Cus_b%3A10&$=3200000
Holdings as pasted by the treasurer:
(see share link — the plan's default target-date fund modeled on the calculator)
Total amount: $3,200,000
Scope basis requested: Scope 1+2
Largest reallocation the committee would consider: 10 points
```

## Brief

---

## **Northside Co-op 401(k) Plan Default Fund: Carbon Footprint Brief**

### **Headline**

The plan's $3.2 million in default target-date assets finances **253.8 tCO2e per year** (Scope 1+2: direct operations and purchased energy), with a range of 202.9–319.0 tonnes reflecting uncertainty in the underlying intensity estimates.

### **What that means**

This is equivalent to the annual emissions from approximately **55 passenger vehicles**, or **16 average American personal footprints**. The 60 employees' pooled savings, as currently allocated, sits at the *upper end* of the range for Vanguard target-date funds with similar risk levels (201.9–253.8 tCO2e on the same $3.2 million); a higher-bond-weight portfolio would be lower. For context, the fossil-vs-clean intensity ratio on a like-for-like Scope 1+2 basis is **9.3× apart**—meaning a dollar in fossil fuels finances roughly nine times more emissions than a dollar in clean energy.

### **Where it comes from**

| Sleeve | Weight | Annual tCO2e | Share of Total | Source |
|--------|--------|--------------|----------------|--------|
| US Equities (S&P 500) | 54.0% | 103.7 | 40.8% | MSCI/Trucost |
| Int'l Developed (EAFE) | 27.0% | 77.8 | 30.6% | MSCI EAFE index |
| Emerging Markets | 9.0% | 54.7 | 21.6% | MSCI EM index |
| US Bonds / Fixed Income | 10.0% | 17.6 | 6.9% | PCAF/GDP alloc |

### **Options the committee could consider**

**Option 1: Reallocate 9 points (all $288,000) from Emerging Markets into Clean Energy**
- Saves **47.5 tCO2e per year** (18.7% reduction → 206.2 tonne total)
- *Caveat:* Moves the entire EM holding; no partial rebalancing among that sleeve.
- Alternates within the 10-point move limit: Real Estate (41.8 t saved), US Bonds (38.9 t saved).

**Option 2: Reallocate 10 points ($320,000) from Int'l Developed into Clean Energy**
- Saves **20.8 tCO2e per year** (8.2% reduction → 233.0 tonne total)
- *Caveat:* Moves a moderate slice of EAFE while leaving Emerging Markets, the highest-intensity sleeve, unchanged.
- Alternates: Real Estate (14.4 t saved), US Bonds (11.2 t saved).

**Option 3: Reallocate 10 points ($320,000) from US Equities into Clean Energy**
- Saves **11.2 tCO2e per year** (4.4% reduction → 242.6 tonne total)
- *Caveat:* Smallest reduction of the three; US Equities carry lower intensity than developed or emerging markets, so the carbon benefit is marginal.
- Alternates: Real Estate (4.8 t saved), US Bonds (1.6 t saved).

**Carbon-only disclaimer:** These options are ranked by tonnes saved and do not model return, risk, fees, liquidity or fiduciary constraints—a committee should weigh them with its investment advisor or policy statement before acting.

### **How sure is this**

**Scope basis:** Scope 1+2 (direct operations and purchased energy), the same basis for every asset class. Scope 3 (estimated indirect supply-chain emissions) can be added on request; it would typically multiply these figures by 2× for equities and bonds, 3× for fossil fuels.

**Band:** The 202.9–319.0 tonne range reflects the spread of the underlying intensity estimates (low to high for each asset class applied to the same weights)—not a statistical confidence interval. It shows what happens if real holdings hit the pessimistic or optimistic end of cited ranges.

**Limitation:** These are asset-class averages. The model does not use fund-level or company-level carbon data, so it cannot distinguish two funds in the US Equities sleeve (e.g., a broad S&P 500 fund vs. a fossil-free equity fund). If the committee later selects specific funds, their true intensities may differ.

**Sources:**
- **MSCI/Trucost** (Apr 2024), *Carbon Footprinting Demystified* — US Equities at 60 t/M (50–75 range).
- **MSCI EAFE Index** — Int'l Developed at 90 t/M (70–110 range); Emerging Markets at 190 t/M (150–250 range).
- **PCAF Global GHG Accounting & Reporting Standard for the Financial Industry** — US Bonds at 55 t/M (40–70 range); Clean Energy at 25 t/M (15–40 range).
- **EPA Household Carbon Footprint Calculator** — Average American at ~16 tCO2e/year; passenger vehicle at ~4.6 tCO2e/year.

---

**Prepared for Northside Co-op 401(k) Committee, 4 sleeves parsed, 0 unassessed.**


## Machine check (brief vs. tool results)

- ✅ footprint computed on the parsed allocation (match)
- ✅ footprint computed at the real total $3,200,000 (got 3200000)
- ✅ scope basis matches profile (scope3=False)
- ✅ headline total 253.76 appears
- ✅ band 202.88–319.04 appears
- ✅ calculate_financed_emissions called once (was 1)
- ✅ breakdown us_equities = 103.68 appears
- ✅ breakdown intl_developed = 77.76 appears
- ✅ breakdown emerging_markets = 54.72 appears
- ✅ breakdown us_bonds = 17.6 appears
- ✅ option emerging_markets→clean_energy saves 47.52 appears
- ✅ option intl_developed→clean_energy saves 20.8 appears
- ✅ option us_equities→clean_energy saves 11.2 appears
- ✅ carbon-only disclaimer present
- ✅ scope basis stated

## Tool trace (verbatim)

### parse_share_link

**input**
```json
{
 "url": "https://carbon-footprint-calc-wine.vercel.app/#a=us_%3A54%2Cint%3A27%2Ceme%3A9%2Cus_b%3A10&$=3200000"
}
```
**result**
```json
{
 "allocation": {
  "us_equities": 54.0,
  "intl_developed": 27.0,
  "emerging_markets": 9.0,
  "us_bonds": 10.0
 },
 "amount_usd": 3200000.0,
 "scope3": false,
 "valid": true
}
```

### calculate_financed_emissions

**input**
```json
{
 "holdings_text": "https://carbon-footprint-calc-wine.vercel.app/#a=us_%3A54%2Cint%3A27%2Ceme%3A9%2Cus_b%3A10&$=3200000",
 "amount_usd": 3200000,
 "scope3": false
}
```
**result**
```json
{
 "scope_basis": "Scope 1+2 (direct operations + purchased energy), every asset class on the same basis",
 "allocation_used": {
  "us_equities": 54.0,
  "intl_developed": 27.0,
  "emerging_markets": 9.0,
  "us_bonds": 10.0
 },
 "parsed": {
  "unmapped": [],
  "mapped_pct": 100.0,
  "unmapped_pct": 0.0,
  "note": "Allocation decoded from a calculator share link."
 },
 "amount_usd": 3200000.0,
 "allocated_pct": 100.0,
 "unallocated_pct": 0.0,
 "tco2e_per_year": 253.76,
 "band_low": 202.88,
 "band_high": 319.04,
 "band_note": "Low/high apply each class's low/high intensity estimate to the same weights \u2014 the spread of the inputs, not a statistical confidence interval.",
 "equivalents": {
  "passenger_cars": 55.2,
  "average_american_personal_footprints": 15.86,
  "ny_la_round_trips": 282
 },
 "breakdown": [
  {
   "class": "us_equities",
   "name": "US Equities (S&P 500)",
   "weight_pct": 54.0,
   "amount_usd": 1728000,
   "intensity_t_per_musd": 60,
   "tco2e_per_year": 103.68,
   "source": "MSCI/Trucost",
   "scope3_multiplier": 2
  },
  {
   "class": "intl_developed",
   "name": "Int'l Developed (EAFE)",
   "weight_pct": 27.0,
   "amount_usd": 864000,
   "intensity_t_per_musd": 90,
   "tco2e_per_year": 77.76,
   "source": "MSCI EAFE index",
   "scope3_multiplier": 2
  },
  {
   "class": "emerging_markets",
   "name": "Emerging Markets",
   "weight_pct": 9.0,
   "amount_usd": 288000,
   "intensity_t_per_musd": 190,
   "tco2e_per_year": 54.72,
   "source": "MSCI EM index",
   "scope3_multiplier": 2
  },
  {
   "class": "us_bonds",
   "name": "US Bonds / Fixed Income",
   "weight_pct": 10.0,
   "amount_usd": 320000,
   "intensity_t_per_musd": 55,
   "tco2e_per_year": 17.6,
   "source": "PCAF/GDP alloc",
   "scope3_multiplier": 2
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
 "amount_usd": 3200000,
 "scope3": false
}
```
**result**
```json
{
 "scope_basis": "Scope 1+2 (direct operations + purchased energy), every asset class on the same basis",
 "target_date_fund_range_tco2e": {
  "low": 201.92,
  "high": 253.76,
  "note": "What the same $3,200,000 would finance in a Vanguard target-date fund, across all nine glide-path presets (younger = more equities = higher)."
 },
 "per_preset_tco2e": {
  "2070 (20)": 253.76,
  "2060 (30)": 253.76,
  "2050 (40)": 253.76,
  "2045 (45)": 251.52,
  "2040 (50)": 243.04,
  "2035 (55)": 235.52,
  "2030 (60)": 226.88,
  "2025 (65)": 218.24,
  "Income (72)": 201.92
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
 "holdings_text": "https://carbon-footprint-calc-wine.vercel.app/#a=us_%3A54%2Cint%3A27%2Ceme%3A9%2Cus_b%3A10&$=3200000",
 "amount_usd": 3200000,
 "max_points": 10,
 "scope3": false
}
```
**result**
```json
{
 "allocation_used": {
  "us_equities": 54.0,
  "intl_developed": 27.0,
  "emerging_markets": 9.0,
  "us_bonds": 10.0
 },
 "baseline_tco2e": 253.76,
 "max_points_moved": 10.0,
 "options": [
  {
   "move_points": 9.0,
   "move_usd": 288000,
   "from": "emerging_markets",
   "from_name": "Emerging Markets",
   "to": "clean_energy",
   "to_name": "Clean Energy",
   "tco2e_saved_per_year": 47.52,
   "pct_reduction": 18.7,
   "new_total_tco2e": 206.24,
   "capped_by_holding": true,
   "alternate_destinations": [
    {
     "to": "real_estate",
     "tco2e_saved_per_year": 41.76
    },
    {
     "to": "us_bonds",
     "tco2e_saved_per_year": 38.88
    },
    {
     "to": "us_equities",
     "tco2e_saved_per_year": 37.44
    },
    {
     "to": "intl_developed",
     "tco2e_saved_per_year": 28.8
    }
   ]
  },
  {
   "move_points": 10.0,
   "move_usd": 320000,
   "from": "intl_developed",
   "from_name": "Int'l Developed (EAFE)",
   "to": "clean_energy",
   "to_name": "Clean Energy",
   "tco2e_saved_per_year": 20.8,
   "pct_reduction": 8.2,
   "new_total_tco2e": 232.96,
   "capped_by_holding": false,
   "alternate_destinations": [
    {
     "to": "real_estate",
     "tco2e_saved_per_year": 14.4
    },
    {
     "to": "us_bonds",
     "tco2e_saved_per_year": 11.2
    },
    {
     "to": "us_equities",
     "tco2e_saved_per_year": 9.6
    }
   ]
  },
  {
   "move_points": 10.0,
   "move_usd": 320000,
   "from": "us_equities",
   "from_name": "US Equities (S&P 500)",
   "to": "clean_energy",
   "to_name": "Clean Energy",
   "tco2e_saved_per_year": 11.2,
   "pct_reduction": 4.4,
   "new_total_tco2e": 242.56,
   "capped_by_holding": false,
   "alternate_destinations": [
    {
     "to": "real_estate",
     "tco2e_saved_per_year": 4.8
    },
    {
     "to": "us_bonds",
     "tco2e_saved_per_year": 1.6
    }
   ]
  },
  {
   "move_points": 10.0,
   "move_usd": 320000,
   "from": "us_bonds",
   "from_name": "US Bonds / Fixed Income",
   "to": "clean_energy",
   "to_name": "Clean Energy",
   "tco2e_saved_per_year": 9.6,
   "pct_reduction": 3.8,
   "new_total_tco2e": 244.16,
   "capped_by_holding": false,
   "alternate_destinations": [
    {
     "to": "real_estate",
     "tco2e_saved_per_year": 3.2
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

