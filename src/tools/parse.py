"""Turn what a volunteer treasurer actually has — a pasted statement, a list of tickers, a
sentence, or a calculator share link — into a sleeve allocation. Unmapped holdings are returned
by name with their weight; the agent must report them as unassessed, never absorb them."""
from __future__ import annotations

import re
from urllib.parse import parse_qs, unquote, urlparse

from strands import tool

from src.model import C, V
from src.tickers import PHRASES, TICKERS

_PCT = re.compile(r"(\d+(?:\.\d+)?)\s*%")
_USD = re.compile(r"\$\s?([\d,]+(?:\.\d+)?)\s*([kKmM])?")
_TICKER = re.compile(r"\b([A-Z]{2,5})\b")
_SPLIT = re.compile(r"[\n;,]+|\s{2,}|\s+\band\b\s+|\s+\bplus\b\s+")


def _resolve(target, weight: float, alloc: dict) -> None:
    if isinstance(target, str):
        alloc[target] = alloc.get(target, 0) + weight
    elif isinstance(target, dict):
        for k, f in target.items():
            alloc[k] = alloc.get(k, 0) + weight * f
    elif isinstance(target, tuple) and target[0] == "preset":
        for k, p in V[target[1]].items():
            alloc[k] = alloc.get(k, 0) + weight * p / 100


def _classify(segment: str):
    """Return (target, label) for a segment, or (None, None)."""
    for tk in _TICKER.findall(segment):
        if tk in TICKERS:
            return TICKERS[tk], tk
    low = segment.lower()
    for phrase, target in PHRASES:  # PHRASES is ordered most-specific first
        if phrase in low:
            return target, phrase
    return None, None


def parse_holdings_text(text: str) -> dict:
    # protect thousands separators ("$38,000") before splitting on commas
    cleaned = re.sub(r"(?<=\d),(?=\d{3}\b)", "", text or "")
    segments = [s.strip() for s in _SPLIT.split(cleaned) if s and s.strip()]
    rows = []
    for seg in segments:
        pct = _PCT.search(seg)
        usd = _USD.search(seg)
        if not pct and not usd:
            continue
        amount = None
        if usd:
            amount = float(usd.group(1).replace(",", ""))
            if usd.group(2):
                amount *= 1e3 if usd.group(2).lower() == "k" else 1e6
        target, label = _classify(seg)
        rows.append({"segment": seg, "pct": float(pct.group(1)) if pct else None, "usd": amount, "target": target, "label": label})
    if not rows:
        return {"allocation": {}, "unmapped": [], "mapped_pct": 0.0, "unmapped_pct": 0.0, "amount_usd": None, "rows": 0,
                "note": "No percentages or dollar amounts found. Each holding needs a % or a $ figure."}

    total_usd = sum(r["usd"] for r in rows if r["usd"]) if all(r["usd"] for r in rows) else None
    if total_usd:  # dollar statement → weights from dollars
        for r in rows:
            r["pct"] = r["usd"] / total_usd * 100
    alloc: dict = {}
    unmapped = []
    for r in rows:
        if r["pct"] is None:
            continue
        if r["target"] is None:
            unmapped.append({"holding": r["segment"], "pct": round(r["pct"], 2)})
        else:
            _resolve(r["target"], r["pct"], alloc)
    alloc = {k: round(v, 2) for k, v in alloc.items() if k in C and v > 0}
    mapped = round(sum(alloc.values()), 2)
    un = round(sum(u["pct"] for u in unmapped), 2)
    return {"allocation": alloc, "unmapped": unmapped, "mapped_pct": mapped, "unmapped_pct": un,
            "amount_usd": total_usd, "rows": len(rows),
            "note": ("Weights derived from dollar amounts." if total_usd else "Weights taken as stated percentages.")
                    + (" Unmapped holdings carry NO carbon estimate and must be reported as unassessed." if unmapped else "")}


@tool
def parse_allocation(holdings_text: str) -> dict:
    """Parse a pasted statement, ticker list, or plain sentence into asset-class weights.

    Accepts lines like "VTI 60%", "$120,000 in BND", "30% international stocks", "10% cash",
    or a Vanguard target-date ticker (e.g. "VFIFX 100%"). Returns the sleeve allocation (percent
    by class), the list of holdings it could NOT map (with their weight, so they can be reported
    as unassessed), how much of the portfolio was mapped, and the total dollar amount if the text
    was in dollars. Never guesses a sleeve for an unknown fund.

    Args:
        holdings_text: The raw text the treasurer pasted.
    """
    return parse_holdings_text(holdings_text)


def parse_share_link_str(url: str) -> dict:
    """Decode a carbon-footprint-calc share link: #a=us_:54,int:27,...&$=1000000[&s=3]."""
    frag = urlparse(url).fragment or (url.split("#", 1)[1] if "#" in url else url)
    q = parse_qs(frag, keep_blank_values=True)
    a = unquote(q.get("a", [""])[0])
    amount = float(q.get("$", ["0"])[0] or 0)
    scope3 = q.get("s", [""])[0] == "3"
    alloc: dict = {}
    for pair in filter(None, a.split(",")):
        short, _, v = pair.partition(":")
        key = next((k for k in C if k.startswith(short)), None)
        if key:
            try:
                alloc[key] = float(v)
            except ValueError:
                pass
    return {"allocation": alloc, "amount_usd": amount, "scope3": scope3, "valid": bool(alloc)}


def resolve_allocation(text: str) -> dict:
    """Text or share link → the parse result. Deterministic; the compute tools call this so the
    model never has to retype an allocation."""
    if "#a=" in (text or "") or "a=" in (text or "") and "%3A" in (text or ""):
        r = parse_share_link_str(text.strip())
        return {"allocation": r["allocation"], "unmapped": [], "mapped_pct": round(sum(r["allocation"].values()), 2),
                "unmapped_pct": 0.0, "amount_usd": r["amount_usd"] or None, "scope3": r["scope3"], "rows": len(r["allocation"]),
                "note": "Allocation decoded from a calculator share link."}
    r = parse_holdings_text(text)
    r["scope3"] = False
    return r


@tool
def parse_share_link(url: str) -> dict:
    """Decode a share link copied from carbon-footprint-calc-wine.vercel.app.

    The link encodes the allocation, amount, and scope basis in its hash. Returns the same
    allocation shape parse_allocation returns, plus amount_usd and whether Scope 3 was on.

    Args:
        url: The full share URL (or just its #fragment).
    """
    return parse_share_link_str(url)
