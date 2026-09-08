"""Ranked reallocation options, carbon-only. The agent may only propose moving money INTO
sleeves the model can source (never fossil fuels, crypto, or cash), and must say every time that this
is a carbon calculation, not investment advice — risk, return, fees and fiduciary duty are not
modeled here and belong with the committee's advisor."""
from __future__ import annotations

from strands import tool

from src.guards import allocation_error
from src.tools.parse import resolve_allocation
from src.model import C, SHIFT_TARGETS, em, intensity

CARBON_ONLY_NOTE = ("Carbon-only analysis from asset-class average intensities. It does not model return, risk, fees, "
                    "liquidity or fiduciary constraints — a committee should weigh these options with its investment "
                    "advisor or policy statement before acting.")


def rank_shift_options(allocation: dict | None, amount_usd: float | None, max_points: float = 10, scope3: bool = False, top_n: int = 5,
                       holdings_text: str = "") -> dict:
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
    alloc = {k: float(v) for k, v in (allocation or {}).items() if k in C and float(v) > 0}
    m = amount_usd / 1e6
    base = em(alloc, m, scope3)
    options = []
    for frm, held in alloc.items():
        i_from = intensity(frm, scope3)
        for to in SHIFT_TARGETS:
            if to == frm:
                continue
            i_to = intensity(to, scope3)
            if i_to >= i_from:
                continue
            pts = min(max_points, held)
            saved = pts / 100 * m * (i_from - i_to)
            new = dict(alloc); new[frm] = held - pts; new[to] = new.get(to, 0) + pts
            options.append({
                "move_points": round(pts, 2), "move_usd": round(pts / 100 * amount_usd), "from": frm, "from_name": C[frm]["name"], "to": to, "to_name": C[to]["name"],
                "tco2e_saved_per_year": round(saved, 2), "pct_reduction": round(saved / base * 100, 1) if base else 0.0,
                "new_total_tco2e": round(em(new, m, scope3), 2),
                "capped_by_holding": pts < max_points,
            })
    options.sort(key=lambda o: -o["tco2e_saved_per_year"])
    # One option per SOURCE sleeve (its best destination), so the committee sees distinct moves
    # instead of five variants of the same one. Alternates are kept on the option.
    best: dict = {}
    for o in options:
        if o["from"] not in best:
            o["alternate_destinations"] = []
            best[o["from"]] = o
        else:
            best[o["from"]]["alternate_destinations"].append({"to": o["to"], "tco2e_saved_per_year": o["tco2e_saved_per_year"]})
    options = list(best.values())
    return {
        "allocation_used": alloc,
        "baseline_tco2e": round(base, 2),
        "max_points_moved": max_points,
        "options": options[:top_n],
        "options_considered": sum(1 + len(o["alternate_destinations"]) for o in options),
        "never_proposed_as_destination": ["fossil_fuels", "crypto", "cash (an exit, not a reallocation)"],
        "note": CARBON_ONLY_NOTE,
    }


@tool
def rank_shifts(holdings_text: str, amount_usd: float | None = None, max_points: float = 10, scope3: bool = False) -> dict:
    """Rank single reallocation moves by tCO2e saved per year, carbon-only.

    For each sleeve the portfolio holds, considers moving up to `max_points` percentage points
    into every lower-intensity INVESTMENT sleeve the model can source (never into fossil fuels,
    crypto, or cash — cash would top every ranking but is an exit, not a reallocation).
    Returns one option per held sleeve (its best destination, alternates attached), ranked by
    tonnes saved, with percent reduction and the new total, plus the
    mandatory carbon-only disclaimer that MUST appear next to any option in the brief.

    Args:
        holdings_text: The raw pasted holdings, or a share link — the SAME text you gave
            calculate_financed_emissions, verbatim. The tool parses it itself.
        amount_usd: Total dollars in the portfolio. Omit if the text is in dollars.
        max_points: Largest move to consider, in percentage points of the whole portfolio.
        scope3: Must match the scope basis used for the footprint.
    """
    return rank_shift_options(None, amount_usd, max_points, scope3, holdings_text=holdings_text)
