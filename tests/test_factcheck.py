import io, json
from src.factcheck import continuity_check, factual_sentences, render_section

BRIEF = """The Vanguard target-date fund range for $2.4 million is 151–190 tCO2e per year.
The 129.7–217.0 tCO2e range reflects the low and high estimates for each asset class held at the same weights.
**Headline** — The endowment finances 155 tCO2e/yr (range 124–196).
Bitcoin network emissions are 39.8 MtCO2e per year according to the Cambridge Digital Mining Industry Report (April 2025).
Bitcoin market capitalization was $1.578 trillion per CoinGecko on 2026-09-08.
The average American personal footprint is about 16 tCO2e per year (EPA).
Moving 10 points from US equities into clean energy would cut 7.9 tCO2e per year.
MSCI's Carbon Footprinting Demystified (April 2024) defines WACI as tCO2e per $M revenue.
"""


def test_factual_sentences_keep_sourced_facts_and_skip_own_math():
    s = factual_sentences(BRIEF)
    assert any("Cambridge" in x for x in s) and any("CoinGecko" in x for x in s) and any("MSCI" in x for x in s)
    assert not any("Moving 10 points" in x for x in s)          # the Steward's own arithmetic is not a web fact
    assert not any(x.startswith("Headline") for x in s)
    assert not any("$2.4 million" in x or "range reflects" in x for x in s)   # brief-internal figures are not web facts


def test_continuity_check_posts_analyst_script_and_parses_rows():
    seen = {}

    class Resp(io.BytesIO):
        def __enter__(self): return self
        def __exit__(self, *a): return False

    def opener(req, timeout):
        seen["url"] = req.full_url; seen["body"] = json.loads(req.data)
        return Resp(json.dumps([{"claim": "x", "verdict": "CONFIRMED", "reasoning": "r", "sources": [{"url": "https://s", "title": "t"}]}]).encode())

    rows = continuity_check(["Bitcoin emits 39.8 MtCO2e per year (Cambridge, 2025)."], base_url="https://cc.example", opener=opener)
    assert seen["url"] == "https://cc.example/check-agent" and seen["body"]["script"].startswith("ANALYST: ")
    assert rows[0]["verdict"] == "CONFIRMED"
    assert continuity_check([], opener=opener) == []


def test_render_section_counts_and_flags_contradictions():
    md = render_section([{"claim": "a", "verdict": "CONFIRMED", "reasoning": "ok", "sources": [{"url": "https://s"}]},
                         {"claim": "b", "verdict": "CONTRADICTED", "reasoning": "no", "sources": []}], base_url="https://cc")
    assert "CONFIRMED: 1" in md and "CONTRADICTED: 1" in md and "**CONTRADICTED** — b" in md and "re-check that input" in md
