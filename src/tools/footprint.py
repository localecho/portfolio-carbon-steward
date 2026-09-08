"""The number, its band, and where it sits — all from src/model.py, nothing invented here."""
from __future__ import annotations

from strands import tool

from src.guards import allocation_error
from src.tools.parse import resolve_allocation
from src.model import (AVG_AMERICAN_T, BTC_DEFAULTS, C, ScopeBasis, TDF_KEYS, V, band, em,
                       equivalents, intensity, lever_ratio, preset_range, table)


def compute_footprint(allocation: dict | None, amount_usd: float | None, scope3: bool = False,
                      btc_mt_per_year: float | None = None, btc_market_cap_usd: float | None = None,
                      holdings_text: str = "") -> dict:
    parsed = None
    if holdings_text:
        parsed = resolve_allocation(holdings_text)
        allocation = parsed["allocation"]
        if not amount_usd and parsed.get("amount_usd"):
            amount_usd = parsed["amount_usd"]
        if parsed.get("scope3"):
            scope3 = True
    err = allocation_error(allocation, amount_usd)
    if err:
        return {"error": err}
    tbl = table(btc_mt_per_year, btc_market_cap_usd)
    m = amount_usd / 1e6
    alloc = {k: float(v) for k, v in (allocation or {}).items() if k in tbl and float(v) > 0}
    total_pct = round(sum(alloc.values()), 2)
    b = band(alloc, m, scope3, tbl)
    rows = []
    for k, p in sorted(alloc.items(), key=lambda kv: -intensity(kv[0], scope3, "t", tbl) * kv[1]):
        i = intensity(k, scope3, "t", tbl)
        rows.append({"class": k, "name": tbl[k]["name"], "weight_pct": round(p, 2), "amount_usd": round(m * p / 100 * 1e6),
                     "intensity_t_per_musd": round(i, 1), "tco2e_per_year": round(i * m * p / 100, 2),
                     "source": tbl[k]["src"], "scope3_multiplier": tbl[k]["s3"]})
    eq = equivalents(b["t"])
    return {
        "scope_basis": ScopeBasis(scope3).label,
        "allocation_used": alloc,
        "parsed": ({"unmapped": parsed["unmapped"], "mapped_pct": parsed["mapped_pct"], "unmapped_pct": parsed["unmapped_pct"], "note": parsed["note"]} if parsed else None),
        "amount_usd": amount_usd,
        "allocated_pct": total_pct,
        "unallocated_pct": round(100 - total_pct, 2),
        "tco2e_per_year": round(b["t"], 2),
        "band_low": round(b["lo"], 2), "band_high": round(b["hi"], 2),
        "band_note": "Low/high apply each class's low/high intensity estimate to the same weights — the spread of the inputs, not a statistical confidence interval.",
        "equivalents": {"passenger_cars": round(eq["cars"], 1), "average_american_personal_footprints": round(eq["americans"], 2), "ny_la_round_trips": round(eq["flights"])},
        "breakdown": rows,
        "method": "E = Σ w_i × A × I_i ; I_i = tCO2e per $1M invested (asset-class averages, not fund-level data)",
        "bitcoin_inputs": {"mt_per_year": btc_mt_per_year or BTC_DEFAULTS["mt_per_year"], "market_cap_usd": btc_market_cap_usd or BTC_DEFAULTS["market_cap_usd"], "as_of": BTC_DEFAULTS["as_of"]} if "crypto" in alloc else None,
    }


@tool
def calculate_financed_emissions(holdings_text: str, amount_usd: float | None = None, scope3: bool = False) -> dict:
    """Compute the portfolio's financed emissions (tCO2e per year) with an uncertainty band.

    Pass the treasurer's holdings text (or calculator share link) VERBATIM — the tool parses it
    itself, deterministically, so the allocation can never be mistyped. Uses the same model as
    carbon-footprint-calc-wine.vercel.app: E = Σ weight × amount × class intensity. Returns the
    allocation actually used, what could not be mapped, the central estimate, the low–high band,
    per-class breakdown with sources, everyday equivalents, and the scope basis string that MUST
    be repeated in any brief.

    Args:
        holdings_text: The raw pasted holdings, or a share link. Copy it exactly.
        amount_usd: Total dollars in the portfolio. Omit if the text is in dollars.
        scope3: False = Scope 1+2 (default, like-for-like). True = add the estimated Scope 3 uplift.
    """
    return compute_footprint(None, amount_usd, scope3, holdings_text=holdings_text)


def reference_points(amount_usd: float, scope3: bool = False) -> dict:
    m = amount_usd / 1e6
    pr = preset_range(scope3)
    return {
        "scope_basis": ScopeBasis(scope3).label,
        "target_date_fund_range_tco2e": {"low": round(pr["min"] * m, 2), "high": round(pr["max"] * m, 2),
                                         "note": f"What the same ${amount_usd:,.0f} would finance in a Vanguard target-date fund, across all nine glide-path presets (younger = more equities = higher)."},
        "per_preset_tco2e": {k: round(em(V[k], m, scope3), 2) for k in TDF_KEYS},
        "average_american_personal_footprint_tco2e": AVG_AMERICAN_T,
        "fossil_vs_clean_lever": {"fossil_t_per_musd": round(intensity("fossil_fuels", scope3), 1), "clean_t_per_musd": round(intensity("clean_energy", scope3), 1), "ratio": round(lever_ratio(scope3), 1)},
    }


@tool
def compare_to_reference(amount_usd: float, scope3: bool = False) -> dict:
    """Reference points to put a footprint in context, at the same dollar amount and scope basis.

    Returns what the same dollars would finance in each Vanguard target-date fund (the default
    for most 401(k) savers), the average American's personal footprint, and the like-for-like
    fossil-vs-clean intensity ratio. Use it so the committee sees "typical" next to "yours".

    Args:
        amount_usd: Total dollars in the portfolio.
        scope3: Must match the scope basis used for the footprint.
    """
    return reference_points(amount_usd, scope3)
