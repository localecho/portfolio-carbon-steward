/* Carbon Footprint of Capital — pure model (no DOM).
 * Loaded by index.html as <script src="model.js"> (attaches window.CFC)
 * and by tests via require('../model.js'). Keep this file free of DOM access.
 *
 * Scope convention (v2): every `t/lo/hi` is Scope 1+2 so classes compare
 * apples-to-apples. `s3` is the multiplier applied when the user opts into
 * an estimated Scope 3 view — the page's own footnote rule: "including
 * Scope 3 roughly doubles most figures and triples fossil fuels".
 * Fossil fuels were previously stored as 700 (Scope 1+2+3) next to Scope 1+2
 * peers; 700/3 ≈ 233 is that same number brought onto the common basis.
 */
(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else root.CFC = factory();
})(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  const AVG_AMERICAN_T = 16;   // tCO2e/yr, EPA/World Bank order of magnitude
  const CAR_T = 4.6;           // EPA typical passenger vehicle
  const FLIGHT_T = 0.9;        // NY–LA round trip, economy

  // Bitcoin: financed emissions per $M = network emissions ÷ market cap.
  // Defaults are dated; the page exposes both inputs so the reader can update them.
  const BTC_DEFAULTS = {
    mt_per_year: 39.8,       // Cambridge Digital Mining Industry Report, Apr 2025 (32.9–39.8 MtCO2e)
    mt_low: 32.9,
    market_cap_usd: 1.578e12 // CoinGecko, 2026-09-08
  };

  function cryptoIntensity(mtPerYear, marketCapUsd) {
    if (!(mtPerYear > 0) || !(marketCapUsd > 0)) return 0;
    return (mtPerYear * 1e6) / (marketCapUsd / 1e6); // t per $M invested
  }

  const btcT = cryptoIntensity(BTC_DEFAULTS.mt_per_year, BTC_DEFAULTS.market_cap_usd);
  const btcLo = cryptoIntensity(BTC_DEFAULTS.mt_low, BTC_DEFAULTS.market_cap_usd);
  const btcHi = cryptoIntensity(BTC_DEFAULTS.mt_per_year, BTC_DEFAULTS.market_cap_usd / 2); // price halves → intensity doubles

  const C = {
    us_equities:      { name: "US Equities (S&P 500)",   short: "US Eq",  t: 60,  lo: 50,  hi: 75,  s3: 2, src: "MSCI/Trucost",      color: "#2563eb" },
    intl_developed:   { name: "Int'l Developed (EAFE)",   short: "Int'l",  t: 90,  lo: 70,  hi: 110, s3: 2, src: "MSCI EAFE index",   color: "#7c3aed" },
    emerging_markets: { name: "Emerging Markets",         short: "EM",     t: 190, lo: 150, hi: 250, s3: 2, src: "MSCI EM index",     color: "#b45309" },
    us_bonds:         { name: "US Bonds / Fixed Income",  short: "Bonds",  t: 55,  lo: 40,  hi: 70,  s3: 2, src: "PCAF/GDP alloc",    color: "#4338ca" },
    real_estate:      { name: "Real Estate / REITs",      short: "RE",     t: 45,  lo: 30,  hi: 60,  s3: 2, src: "PCAF/FTSE Nareit",  color: "#0f766e" },
    fossil_fuels:     { name: "Fossil Fuels",             short: "Fossil", t: 233, lo: 133, hi: 300, s3: 3, src: "Trucost/CDP (700 ÷ 3)", color: "#b91c1c" },
    clean_energy:     { name: "Clean Energy",             short: "Clean",  t: 25,  lo: 15,  hi: 40,  s3: 2, src: "S&P Clean Energy",  color: "#15803d" },
    cash:             { name: "Cash / Money Market",      short: "Cash",   t: 2,   lo: 0,   hi: 5,   s3: 1, src: "PCAF (zero)",       color: "#6b7280" },
    crypto:           { name: "Crypto / Bitcoin",         short: "BTC",    t: btcT, lo: btcLo, hi: btcHi, s3: 1, src: "CBECI ÷ market cap", color: "#c2410c", derived: true },
  };

  // Vanguard Target Retirement glide path → four sleeves (intl split 75/25 dev/EM).
  const V = {
    "2070 (20)":   { us_equities: 54,   intl_developed: 27,    emerging_markets: 9,    us_bonds: 10 },
    "2060 (30)":   { us_equities: 54,   intl_developed: 27,    emerging_markets: 9,    us_bonds: 10 },
    "2050 (40)":   { us_equities: 54,   intl_developed: 27,    emerging_markets: 9,    us_bonds: 10 },
    "2045 (45)":   { us_equities: 52,   intl_developed: 26.25, emerging_markets: 8.75, us_bonds: 13 },
    "2040 (50)":   { us_equities: 47,   intl_developed: 23.25, emerging_markets: 7.75, us_bonds: 22 },
    "2035 (55)":   { us_equities: 41.5, intl_developed: 20.6,  emerging_markets: 6.9,  us_bonds: 31 },
    "2030 (60)":   { us_equities: 35.5, intl_developed: 17.6,  emerging_markets: 5.9,  us_bonds: 41 },
    "2025 (65)":   { us_equities: 29.5, intl_developed: 14.6,  emerging_markets: 4.9,  us_bonds: 51 },
    "Income (72)": { us_equities: 18,   intl_developed: 9,     emerging_markets: 3,    us_bonds: 70 },
    "All Fossil":  { fossil_fuels: 100 },
    "All Clean":   { clean_energy: 100 },
  };
  const TDF_KEYS = Object.keys(V).slice(0, 9);

  const STRATA = [
    { age: "<25",   med: 1800,   fund: "2070",   preset: "2070 (20)" },
    { age: "25-34", med: 18000,  fund: "2065",   preset: "2060 (30)" },
    { age: "35-44", med: 45000,  fund: "2055",   preset: "2060 (30)" },
    { age: "45-54", med: 85000,  fund: "2040",   preset: "2040 (50)" },
    { age: "55-64", med: 120000, fund: "2035",   preset: "2035 (55)" },
    { age: "65-74", med: 165000, fund: "2025",   preset: "2025 (65)" },
    { age: "75+",   med: 120000, fund: "Income", preset: "Income (72)" },
  ];

  // Intensity of one class at the requested scope view. which ∈ {t,lo,hi}.
  function intensity(k, scope3, which) {
    const d = C[k]; if (!d) return 0;
    return d[which || 't'] * (scope3 ? d.s3 : 1);
  }

  // Financed emissions (t/yr) for an allocation (% by class) on m $M.
  function em(alloc, m, scope3, which) {
    let s = 0;
    for (const [k, p] of Object.entries(alloc || {})) if (C[k] && p) s += intensity(k, scope3, which) * m * (p / 100);
    return s;
  }

  function band(alloc, m, scope3) {
    return { lo: em(alloc, m, scope3, 'lo'), t: em(alloc, m, scope3, 't'), hi: em(alloc, m, scope3, 'hi') };
  }

  // Min/max per $1M across the Vanguard presets — drives the "Wealth is the multiplier" finding.
  function presetRange(scope3) {
    const vals = TDF_KEYS.map(k => em(V[k], 1, scope3));
    return { min: Math.min(...vals), max: Math.max(...vals) };
  }

  // Fossil ÷ clean at the requested scope — drives the "Allocation is the lever" finding.
  function leverRatio(scope3) {
    return intensity('fossil_fuels', scope3) / intensity('clean_energy', scope3);
  }

  function largestHeld(alloc) {
    let best = null, bv = 0;
    for (const [k, v] of Object.entries(alloc || {})) if (C[k] && v > bv) { best = k; bv = v; }
    return best;
  }

  function equivalents(total) {
    return { cars: total / CAR_T, americans: total / AVG_AMERICAN_T, flights: total / FLIGHT_T };
  }

  // Re-derive the crypto row from live inputs (page calls this when the reader edits them).
  function setCrypto(mtPerYear, marketCapUsd) {
    C.crypto.t = cryptoIntensity(mtPerYear, marketCapUsd);
    C.crypto.lo = cryptoIntensity(mtPerYear * (BTC_DEFAULTS.mt_low / BTC_DEFAULTS.mt_per_year), marketCapUsd);
    C.crypto.hi = cryptoIntensity(mtPerYear, marketCapUsd / 2);
    return C.crypto.t;
  }

  return { C, V, TDF_KEYS, STRATA, BTC_DEFAULTS, AVG_AMERICAN_T, CAR_T, FLIGHT_T,
           intensity, em, band, presetRange, leverRatio, largestHeld, equivalents, cryptoIntensity, setCrypto };
});
