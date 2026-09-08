"""Optional post-step: hand the brief's factual sentences to Continuity Check
(https://github.com/localecho/continuity-check — Gemini + Parallel Search, live web evidence) and
append a "Live fact-check" section. The Steward's numbers come from a dated lookup table; this step
asks a second, independent system whether the sourced facts still hold on today's web.

Direction is deliberate: the Steward CALLS Continuity Check over HTTP. Continuity Check never imports
or calls the Steward (its hackathon rules restrict it to Google Cloud + Parallel at runtime)."""
from __future__ import annotations

import json
import os
import re
import urllib.request

DEFAULT_URL = os.environ.get("CONTINUITY_CHECK_URL", "https://continuity-check-231147782258.us-central1.run.app")
MAX_CHARS = 7500  # under Continuity Check's 8000-char cap


def factual_sentences(brief: str, max_sentences: int = 12) -> list[str]:
    """Pick sentences that carry a checkable external fact: a number with a unit/date, a named
    source, or a dated input. Skips the brief's own portfolio arithmetic (that is the Steward's
    model, not a web fact)."""
    text = re.sub(r"[*_`#|]", " ", brief)
    sents = re.split(r"(?<=[.!?])\s+", text)
    keep = []
    for s in sents:
        s = " ".join(s.split())
        if len(s) < 30 or len(s) > 300:
            continue
        has_fact = re.search(r"\b(19|20)\d\d\b", s) or re.search(r"\b(MSCI|PCAF|Cambridge|CoinGecko|EPA|Vanguard|World Bank|Nobel|NASA)\b", s) \
            or re.search(r"\b\d+(\.\d+)?\s*(MtCO2e|tCO2e|t/\$M|tonnes|trillion|billion|GB|%)\b", s)
        own_math = (re.search(r"\b(your|the committee'?s|this portfolio|the portfolio|finances|financed|would cut|would save|saves?|saved|new total|percentage points?|points? (from|into|to)|reduction|option)\b", s, re.I)
                    and not re.search(r"\b(MSCI|PCAF|Cambridge|CoinGecko|EPA|Vanguard|World Bank)\b", s))
        # the brief's own portfolio figures are not web facts either: dollar totals, its ranges, its ratios
        own_math = own_math or re.search(r"\$\s?\d[\d,.]*\s*(million|M\b|k\b)|\brange\b.*\b(reflects|applies|shows)\b|\btarget-date fund range\b", s, re.I)
        if has_fact and not own_math:
            keep.append(s)
        if len(keep) >= max_sentences:
            break
    return keep


def continuity_check(sentences: list[str], base_url: str = DEFAULT_URL, timeout: float = 280.0, opener=None) -> list[dict]:
    if not sentences:
        return []
    script = "\n".join(f"ANALYST: {s}" for s in sentences)[:MAX_CHARS]
    req = urllib.request.Request(f"{base_url.rstrip('/')}/check-agent", data=json.dumps({"script": script}).encode(),
                                 headers={"Content-Type": "application/json"}, method="POST")
    opener = opener or urllib.request.urlopen
    with opener(req, timeout=timeout) as r:
        return json.loads(r.read().decode())


def render_section(rows: list[dict], base_url: str = DEFAULT_URL) -> str:
    if not rows:
        return "## Live fact-check (Continuity Check)\n\nNo externally checkable sentences were found in the brief.\n"
    counts = {}
    for r in rows:
        counts[r["verdict"]] = counts.get(r["verdict"], 0) + 1
    lines = ["## Live fact-check (Continuity Check)", "",
             f"_{len(rows)} factual claim(s) from this brief were sent to an independent fact-checker "
             f"(Gemini + Parallel Search, live web evidence) at {base_url}. "
             + " · ".join(f"{k}: {v}" for k, v in sorted(counts.items())) + "._", ""]
    for r in rows:
        srcs = ", ".join(s["url"] for s in r.get("sources", [])[:3])
        lines.append(f"- **{r['verdict']}** — {r['claim']}")
        if r.get("reasoning"):
            lines.append(f"  - {r['reasoning']}")
        if srcs:
            lines.append(f"  - sources: {srcs}")
    lines.append("")
    lines.append("_A CONTRADICTED line means the web disagrees with a source the brief relied on — re-check that input before the committee acts on it._")
    return "\n".join(lines) + "\n"
