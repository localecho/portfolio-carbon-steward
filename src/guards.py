"""Input guards at the tool boundary. A model that passes fractions where percents are expected,
or a per-$1M amount where the real total belongs, gets a clear error to correct — never a
silently wrong number."""
from __future__ import annotations

from src.model import C


def allocation_error(allocation: dict, amount_usd: float) -> str | None:
    if not isinstance(allocation, dict) or not allocation:
        return "allocation must be a non-empty dict of {asset_class: percent}."
    bad = [k for k in allocation if k not in C]
    if bad:
        return f"unknown asset class keys {bad}; valid keys are {list(C)}."
    try:
        vals = [float(v) for v in allocation.values()]
    except (TypeError, ValueError):
        return "allocation values must be numbers (percents, 0–100)."
    total = sum(v for v in vals if v > 0)
    if 0 < total <= 1.5:
        return (f"allocation values sum to {total:.3f} — these look like FRACTIONS. Pass PERCENTS "
                "(e.g. 55 for 55%), exactly as parse_allocation returned them.")
    if total > 100.5:
        return f"allocation values sum to {total:.1f}% (> 100%). Pass the weights exactly as parse_allocation returned them."
    if not (amount_usd and amount_usd > 0):
        return "amount_usd must be a positive dollar total."
    if amount_usd < 500:
        return (f"amount_usd={amount_usd} looks like a per-$1M or per-$1K figure, not a portfolio total. "
                "Pass the committee's total dollars (e.g. 1150000).")
    return None
