"""CLI.  python -m src.run --profile profiles/community_foundation.yaml
        python -m src.run --text "VTI 60%, BND 30%, cash 10%" --amount 850000 --org "Maple St PTA"
Add --save FILE to write the brief (with the tool-call trace) as Markdown."""
from __future__ import annotations

import argparse
import datetime as dt
import os
import sys

import json
import re

from src.agent import build_agent
from src.profile import PortfolioProfile


def run_with_trace(prof: PortfolioProfile):
    """Run the agent and return (brief, tool_calls) where tool_calls = [{name, input, result}]."""
    agent = build_agent()
    brief = str(agent("Here is the committee's profile and holdings:\n\n" + prof.as_prompt_block() + "\n\nProduce the brief per your instructions."))
    calls, pending = [], {}
    for msg in agent.messages:
        for block in msg.get("content", []):
            if "toolUse" in block:
                tu = block["toolUse"]; pending[tu["toolUseId"]] = {"name": tu["name"], "input": tu["input"]}
            if "toolResult" in block:
                tr = block["toolResult"]; c = pending.pop(tr["toolUseId"], {"name": "?", "input": {}})
                txt = "".join(x.get("text", "") for x in tr.get("content", []))
                try: c["result"] = json.loads(txt)
                except Exception: c["result"] = txt
                calls.append(c)
    return brief, calls


def _nums_in(text: str) -> set:
    return {round(float(x.replace(",", "")), 1) for x in re.findall(r"\d[\d,]*\.?\d*", text)}


def verify_brief(brief: str, calls: list, prof: PortfolioProfile | None = None) -> list:
    """Machine check: the tool's headline, band and option figures must appear in the brief.
    Returns a list of (ok, label) — written into the transcript so a reader can see the check."""
    nums = _nums_in(brief)
    def seen(v):
        v = float(v); return round(v, 1) in nums or round(v) in nums or round(v, 2) in nums
    out = []
    fp = [c for c in calls if c["name"] == "calculate_financed_emissions"]
    fp = [c for c in fp if isinstance(c["result"], dict) and "error" not in c["result"]] or fp
    pa = [c for c in calls if c["name"] in ("parse_allocation", "parse_share_link")]
    if fp and pa:  # input fidelity: the number must be computed on what was parsed, at the real total
        want = pa[0]["result"].get("allocation", {})
        got = fp[0]["result"].get("allocation_used") or fp[0]["input"].get("allocation", {})
        same = all(abs(float(got.get(k, 0)) - float(v)) < 0.06 for k, v in want.items()) and set(got) <= set(want) | {k for k, v in got.items() if not v}
        out.append((same, f"footprint computed on the parsed allocation ({'match' if same else f'want {want} got {got}'})"))
        amt_want = (prof.amount_usd if prof and prof.amount_usd else None) or pa[0]["result"].get("amount_usd")
        amt_got = fp[0]["result"].get("amount_usd", fp[0]["input"].get("amount_usd"))  # tool derives it from dollar text
        if amt_want:
            ok_amt = amt_got is not None and abs(float(amt_got) - float(amt_want)) < 1
            out.append((ok_amt, f"footprint computed at the real total ${float(amt_want):,.0f} (got {amt_got})"))
        if prof is not None:
            out.append((bool(fp[0]["input"].get("scope3", False)) == bool(prof.scope3), f"scope basis matches profile (scope3={prof.scope3})"))
    if fp:
        r = fp[0]["result"]
        out.append((seen(r["tco2e_per_year"]), f"headline total {r['tco2e_per_year']} appears"))
        out.append((seen(r["band_low"]) and seen(r["band_high"]), f"band {r['band_low']}–{r['band_high']} appears"))
        out.append((len(fp) == 1, f"calculate_financed_emissions called once (was {len(fp)})"))
        for row in r["breakdown"]:
            out.append((seen(row["tco2e_per_year"]), f"breakdown {row['class']} = {row['tco2e_per_year']} appears"))
    else:
        out.append((False, "calculate_financed_emissions was never called"))
    sh = [c for c in calls if c["name"] == "rank_shifts"]
    if sh:
        for o in sh[-1]["result"]["options"][:3]:
            out.append((seen(o["tco2e_saved_per_year"]), f"option {o['from']}→{o['to']} saves {o['tco2e_saved_per_year']} appears"))
    pa = [c for c in calls if c["name"] == "parse_allocation"]
    if pa and pa[0]["result"].get("unmapped"):
        out.append(("nassessed" in brief, "unassessed section present for unmapped holdings"))
    out.append(("carbon-only" in brief.lower() or "carbon only" in brief.lower(), "carbon-only disclaimer present"))
    out.append(("scope 1+2" in brief.lower(), "scope basis stated"))
    return out


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Portfolio Carbon Steward")
    p.add_argument("--profile", help="YAML profile path")
    p.add_argument("--text", help="pasted holdings text")
    p.add_argument("--amount", type=float, help="total dollars (if --text is in percents)")
    p.add_argument("--org", default="the committee")
    p.add_argument("--scope3", action="store_true", help="add the estimated Scope 3 uplift")
    p.add_argument("--max-points", type=float, default=10)
    p.add_argument("--save", help="write the brief to this Markdown file")
    p.add_argument("--verify", action="store_true", help="send the brief's factual sentences to Continuity Check and append a live fact-check section")
    a = p.parse_args(argv)
    if a.profile:
        prof = PortfolioProfile.from_yaml(a.profile)
    elif a.text:
        prof = PortfolioProfile(name=a.org, org_type="group holding pooled funds", holdings_text=a.text, amount_usd=a.amount,
                                scope3=a.scope3, max_shift_points=a.max_points)
    else:
        p.error("give --profile or --text")
    brief, calls = run_with_trace(prof)
    verify_md = ""
    if a.verify:
        from src.factcheck import continuity_check, factual_sentences, render_section
        try:
            rows = continuity_check(factual_sentences(brief))
            verify_md = render_section(rows)
        except Exception as exc:  # the brief stands on its own; the fact-check is additive
            verify_md = f"## Live fact-check (Continuity Check)\n\n_Unavailable: {exc}_\n"
        brief = brief + "\n\n" + verify_md
    print(brief)
    checks = verify_brief(brief, calls, prof)
    print("\n## Machine check\n" + "\n".join(("PASS " if ok else "FAIL ") + lbl for ok, lbl in checks))
    if a.save:
        with open(a.save, "w") as f:
            f.write(f"# Portfolio Carbon Steward — {prof.name}\n\n")
            f.write(f"_Real run, {dt.datetime.now(dt.timezone.utc):%Y-%m-%d %H:%M UTC}, provider={os.environ.get('STEWARD_MODEL_PROVIDER','openrouter')}, model={os.environ.get('STEWARD_MODEL_ID','anthropic/claude-haiku-4.5')}. Not edited._\n\n")
            f.write("## Input\n\n```\n" + prof.as_prompt_block() + "\n```\n\n## Brief\n\n" + brief + "\n\n")
            f.write("## Machine check (brief vs. tool results)\n\n" + "\n".join(("- ✅ " if ok else "- ❌ ") + lbl for ok, lbl in checks) + "\n\n")
            f.write("## Tool trace (verbatim)\n\n")
            for c in calls:
                f.write(f"### {c['name']}\n\n**input**\n```json\n{json.dumps(c['input'], indent=1)}\n```\n**result**\n```json\n{json.dumps(c['result'], indent=1)[:6000]}\n```\n\n")
    return 0 if all(ok for ok, _ in checks) else 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
