# Demo video script (target 3½–4 min, max 5)

Screen recording + voiceover. Terminal at a large font. Fallback if the live run is slow: scroll
`sample_run_community_foundation.md` — it is a real, unedited transcript.

## 0:00–0:35 — The problem
Over the public calculator page (carbon-footprint-calc-wine.vercel.app), scrolling slowly:
> "A donor asks a community foundation's board: what's the carbon footprint of your endowment?
> Five volunteers, no analyst. The honest answer is a number with a scope basis, an uncertainty
> band, and sources — and nobody in the room can produce one. That's true for PTAs, congregations,
> co-ops, 401(k) committees: groups that hold money together and have nobody whose job this is."

## 0:35–1:00 — Who it's for, what it does
Cut to `profiles/community_foundation.yaml`.
> "Portfolio Carbon Steward is a Strands agent for exactly those groups. The treasurer pastes
> whatever they have — tickers, dollars, plain words, even a share link from the calculator —
> and gets a five-minute brief the committee can act on at its next meeting."

## 1:00–1:20 — Architecture (one diagram)
Show `ARCHITECTURE.md` rendered.
> "Six tools around a pure, tested model. Parse — never guess. Compute with a band. Compare to
> typical. Rank moves, carbon-only. Cite. The same model the public calculator ships, cross-checked
> by tests."

## 1:20–2:50 — Live run
```
.venv/bin/python -m src.run --profile profiles/community_foundation.yaml
```
Narrate the tool calls as they stream, then the brief:
> "It mapped VTI, VXUS, BND, VNQ, XLE — and the CD ladder to cash. Headline: tonnes per year,
> the low–high band, Scope 1+2, on 100% of the portfolio. Context: where it sits against a
> target-date fund at the same dollars. Options: the 4% in the energy-sector fund is small but
> it's the biggest lever per point — and note what the agent does *not* say: it never says 'you
> should'. Carbon-only, advisor's call."

## 2:50–3:30 — The hard case (honesty rails)
```
.venv/bin/python -m src.run --profile profiles/congregation_endowment.yaml
```
> "A congregation with a donated Bitcoin ETF and a 'Legacy Growth Fund' nobody can identify.
> Watch: the unknown fund is listed as unassessed with its 2%, not absorbed. The Bitcoin number
> is derived from dated inputs — network emissions over market cap — and says so. And because
> the committee asked for the Scope 3 view, every number is labeled as an estimate."

## 3:30–3:55 — Why it matters + close
> "Pooled money is where most Americans' financed emissions actually live — not in a personal
> brokerage account, in the 401(k) default fund, the endowment, the reserve. Giving the volunteers
> who steward it an honest number, with the uncertainty attached, is the first step to any
> decision. MIT licensed, Strands SDK, runs on OpenRouter or Bedrock, AgentCore entrypoint
> included. Portfolio Carbon Steward."
