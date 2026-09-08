"""Where every number comes from — so the brief can cite, and the committee can check."""
from __future__ import annotations

from strands import tool

from src.model import BTC_DEFAULTS, C

SOURCES = {
    "MSCI/Trucost": "MSCI, Carbon Footprinting Demystified (Apr 2024) — https://www.msci.com/research-and-insights/paper/carbon-footprinting-demystified",
    "PCAF": "PCAF Global GHG Accounting & Reporting Standard for the Financial Industry — https://carbonaccountingfinancials.com/standard",
    "CBECI": "Cambridge Centre for Alternative Finance, CBECI GHG index — https://ccaf.io/cbnsi/cbeci/ghg ; Cambridge Digital Mining Industry Report (Apr 2025): 39.8 MtCO2e/yr (32.9 under alternative flared-gas assumptions)",
    "CoinGecko": f"Bitcoin market cap ${BTC_DEFAULTS['market_cap_usd']/1e12:.3f}T, CoinGecko, retrieved {BTC_DEFAULTS['as_of']}",
    "Vanguard": "Vanguard Target Retirement glide path (fund prospectuses, 2025); How America Saves 2025 — https://corporate.vanguard.com/content/dam/corp/research/pdf/how_america_saves_report_2025.pdf",
    "EPA": "EPA Household Carbon Footprint Calculator (~16 tCO2e/person/yr; 4.6 tCO2e per passenger vehicle) — https://www.epa.gov/ghgemissions/household-carbon-footprint-calculator",
}


def provenance() -> dict:
    return {
        "scope_convention": "Every class is Scope 1+2 (direct operations + purchased energy). The Scope 3 view multiplies by s3 (×2 most classes, ×3 fossil fuels) as an ESTIMATE per the page's rule of thumb — not reported data.",
        "fossil_fuels_note": "The commonly quoted ~700 t/$M for fossil fuels is Scope 1+2+3. On the common Scope 1+2 basis it is ~233 (700 ÷ 3), so fossil and clean compare like for like: ~9× apart, not 28×.",
        "bitcoin_note": "Derived, not looked up: network MtCO2e ÷ market cap. Price doubles → intensity halves. Inputs are dated; they can be refreshed.",
        "granularity": "Asset-class averages. No fund-level or company-level carbon data is used, so the model cannot distinguish two funds inside the same sleeve.",
        "intensity_table_t_per_musd": {k: {"central": round(d["t"], 1), "low": round(d["lo"], 1), "high": round(d["hi"], 1), "scope3_multiplier": d["s3"], "source": d["src"]} for k, d in C.items()},
        "sources": SOURCES,
        "model_origin": "Same model as carbon-footprint-calc-wine.vercel.app (vendor/model.js, cross-checked by tests).",
    }


@tool
def data_provenance() -> dict:
    """Return the full intensity table with scope convention, sources and dates.

    Call this once per brief so every number the committee reads can be traced to a named,
    dated source, and so the Scope basis and the asset-class-average limitation are stated.
    """
    return provenance()
