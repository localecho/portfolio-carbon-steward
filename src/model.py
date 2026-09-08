"""Financed-emissions model — a faithful Python port of vendor/model.js (the calculator that
ships at carbon-footprint-calc-wine.vercel.app). tests/test_model.py cross-checks every constant
against the vendored JS through node, so the agent can never quietly drift from the page.

Units: intensities are tCO2e per $1M invested, Scope 1+2 for EVERY class. `s3` is the multiplier
applied when a Scope 3 (value-chain) view is requested — the page's own rule of thumb (×2 most
classes, ×3 fossil fuels), labeled as an estimate wherever it is shown.
"""
from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass

AVG_AMERICAN_T = 16.0   # tCO2e/yr personal footprint, EPA/World Bank order of magnitude
CAR_T = 4.6             # EPA typical passenger vehicle, tCO2e/yr
FLIGHT_T = 0.9          # NY–LA round trip, economy

BTC_DEFAULTS = {
    "mt_per_year": 39.8,        # Cambridge Digital Mining Industry Report, Apr 2025
    "mt_low": 32.9,             # same report, alternative flared-gas assumptions
    "market_cap_usd": 1.578e12,  # CoinGecko, 2026-09-08
    "as_of": "2026-09-08",
}


def crypto_intensity(mt_per_year: float, market_cap_usd: float) -> float:
    """Network emissions ÷ market cap → tCO2e per $1M invested. Price doubles → intensity halves."""
    if not (mt_per_year > 0) or not (market_cap_usd > 0):
        return 0.0
    return (mt_per_year * 1e6) / (market_cap_usd / 1e6)


def _base_table() -> dict:
    btc_t = crypto_intensity(BTC_DEFAULTS["mt_per_year"], BTC_DEFAULTS["market_cap_usd"])
    btc_lo = crypto_intensity(BTC_DEFAULTS["mt_low"], BTC_DEFAULTS["market_cap_usd"])
    btc_hi = crypto_intensity(BTC_DEFAULTS["mt_per_year"], BTC_DEFAULTS["market_cap_usd"] / 2)
    return {
        "us_equities":      dict(name="US Equities (S&P 500)",   short="US Eq",  t=60,  lo=50,  hi=75,  s3=2, src="MSCI/Trucost"),
        "intl_developed":   dict(name="Int'l Developed (EAFE)",   short="Int'l",  t=90,  lo=70,  hi=110, s3=2, src="MSCI EAFE index"),
        "emerging_markets": dict(name="Emerging Markets",         short="EM",     t=190, lo=150, hi=250, s3=2, src="MSCI EM index"),
        "us_bonds":         dict(name="US Bonds / Fixed Income",  short="Bonds",  t=55,  lo=40,  hi=70,  s3=2, src="PCAF/GDP alloc"),
        "real_estate":      dict(name="Real Estate / REITs",      short="RE",     t=45,  lo=30,  hi=60,  s3=2, src="PCAF/FTSE Nareit"),
        "fossil_fuels":     dict(name="Fossil Fuels",             short="Fossil", t=233, lo=133, hi=300, s3=3, src="Trucost/CDP (700 ÷ 3)"),
        "clean_energy":     dict(name="Clean Energy",             short="Clean",  t=25,  lo=15,  hi=40,  s3=2, src="S&P Clean Energy"),
        "cash":             dict(name="Cash / Money Market",      short="Cash",   t=2,   lo=0,   hi=5,   s3=1, src="PCAF (zero)"),
        "crypto":           dict(name="Crypto / Bitcoin",         short="BTC",    t=btc_t, lo=btc_lo, hi=btc_hi, s3=1, src="CBECI ÷ market cap", derived=True),
    }


C = _base_table()
CLASS_KEYS = list(C.keys())

# Sleeves the agent may PROPOSE moving money into. Fossil and crypto are never proposed as
# destinations. Cash is excluded too: it "wins" every carbon ranking (2 t/$M) but it is an exit
# from investing, not a reallocation, so it would crowd out every real option.
SHIFT_TARGETS = ["clean_energy", "real_estate", "us_bonds", "us_equities", "intl_developed"]

# Vanguard Target Retirement glide path → four sleeves (international split 75/25 developed/EM).
V = {
    "2070 (20)":   {"us_equities": 54,   "intl_developed": 27,    "emerging_markets": 9,    "us_bonds": 10},
    "2060 (30)":   {"us_equities": 54,   "intl_developed": 27,    "emerging_markets": 9,    "us_bonds": 10},
    "2050 (40)":   {"us_equities": 54,   "intl_developed": 27,    "emerging_markets": 9,    "us_bonds": 10},
    "2045 (45)":   {"us_equities": 52,   "intl_developed": 26.25, "emerging_markets": 8.75, "us_bonds": 13},
    "2040 (50)":   {"us_equities": 47,   "intl_developed": 23.25, "emerging_markets": 7.75, "us_bonds": 22},
    "2035 (55)":   {"us_equities": 41.5, "intl_developed": 20.6,  "emerging_markets": 6.9,  "us_bonds": 31},
    "2030 (60)":   {"us_equities": 35.5, "intl_developed": 17.6,  "emerging_markets": 5.9,  "us_bonds": 41},
    "2025 (65)":   {"us_equities": 29.5, "intl_developed": 14.6,  "emerging_markets": 4.9,  "us_bonds": 51},
    "Income (72)": {"us_equities": 18,   "intl_developed": 9,     "emerging_markets": 3,    "us_bonds": 70},
    "All Fossil":  {"fossil_fuels": 100},
    "All Clean":   {"clean_energy": 100},
}
TDF_KEYS = list(V.keys())[:9]


def table(btc_mt: float | None = None, btc_cap_usd: float | None = None) -> dict:
    """A copy of the intensity table, optionally re-deriving the Bitcoin row from fresh inputs."""
    t = deepcopy(C)
    if btc_mt is not None or btc_cap_usd is not None:
        mt = btc_mt if btc_mt is not None else BTC_DEFAULTS["mt_per_year"]
        cap = btc_cap_usd if btc_cap_usd is not None else BTC_DEFAULTS["market_cap_usd"]
        t["crypto"]["t"] = crypto_intensity(mt, cap)
        t["crypto"]["lo"] = crypto_intensity(mt * BTC_DEFAULTS["mt_low"] / BTC_DEFAULTS["mt_per_year"], cap)
        t["crypto"]["hi"] = crypto_intensity(mt, cap / 2)
    return t


def intensity(k: str, scope3: bool = False, which: str = "t", tbl: dict | None = None) -> float:
    d = (tbl or C).get(k)
    if not d:
        return 0.0
    return d[which] * (d["s3"] if scope3 else 1)


def em(alloc: dict, m: float, scope3: bool = False, which: str = "t", tbl: dict | None = None) -> float:
    """Financed emissions (tCO2e/yr) for an allocation (% by class) on m $M invested."""
    return sum(intensity(k, scope3, which, tbl) * m * (p / 100) for k, p in (alloc or {}).items() if p and k in (tbl or C))


def band(alloc: dict, m: float, scope3: bool = False, tbl: dict | None = None) -> dict:
    return {"lo": em(alloc, m, scope3, "lo", tbl), "t": em(alloc, m, scope3, "t", tbl), "hi": em(alloc, m, scope3, "hi", tbl)}


def preset_range(scope3: bool = False) -> dict:
    vals = [em(V[k], 1, scope3) for k in TDF_KEYS]
    return {"min": min(vals), "max": max(vals)}


def lever_ratio(scope3: bool = False) -> float:
    return intensity("fossil_fuels", scope3) / intensity("clean_energy", scope3)


def largest_held(alloc: dict) -> str | None:
    best, bv = None, 0
    for k, v in (alloc or {}).items():
        if k in C and v > bv:
            best, bv = k, v
    return best


def equivalents(total: float) -> dict:
    return {"cars": total / CAR_T, "americans": total / AVG_AMERICAN_T, "flights": total / FLIGHT_T}


@dataclass(frozen=True)
class ScopeBasis:
    scope3: bool

    @property
    def label(self) -> str:
        return "Scope 1+2 plus an ESTIMATED Scope 3 uplift (×2 most classes, ×3 fossil fuels)" if self.scope3 else "Scope 1+2 (direct operations + purchased energy), every asset class on the same basis"
