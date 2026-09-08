# Devpost submission draft — Agents for Humans Hackathon

Track: **Good Neighbor Agents**

Status: DRAFT. Fill `<REPO_URL>` (repo must be PUBLIC with MIT visible in About) and the video
link (per `VIDEO_SCRIPT.md`) before pasting into the Devpost form. Live demo (optional):
the public calculator https://carbon-footprint-calc-wine.vercel.app is the model's UI; an
AgentCore deployment is wired (`deploy/agentcore_app.py`) but not hosted for this submission.

---

## Project name

**Portfolio Carbon Steward**

## Elevator pitch (one line)

An agent for groups that hold money together and have no analyst: paste the statement, get a
five-minute brief on the carbon the pooled money finances — with the scope basis, the
uncertainty, the sources, and the moves that would cut it most.

## What it does

A donor asks a community foundation's board what the carbon footprint of the endowment is. A
member asks the congregation's committee. An employee asks the 401(k) committee about the
default fund. Five volunteers, no analyst, and the only honest answer is a number that comes
with a scope basis, an uncertainty band, and sources — which nobody in the room can produce.

Portfolio Carbon Steward takes whatever the treasurer can paste — tickers, dollar amounts,
plain words, a Vanguard target-date ticker, or a share link from the public calculator — and,
in one turn:

1. Parses it into asset-class sleeves. Anything it cannot map is **reported as unassessed with
   its weight, never guessed**.
2. Computes financed emissions (tonnes CO2e per year) with a low–high band, on a stated scope
   basis (Scope 1+2 like-for-like by default; an *estimated* Scope 3 view on request).
3. Shows where that sits: the same dollars in each Vanguard target-date fund; the average
   American's personal footprint.
4. Ranks single reallocation moves by tonnes saved — one per held sleeve, never into fossil
   fuels, crypto or cash — and repeats every time that this is carbon-only, not investment
   advice.
5. Cites: the intensity table, the scope convention, named and dated sources.

Four real, unedited runs are in the repo (`sample_run_*.md`), including one with a donated
Bitcoin ETF and an unidentifiable "Legacy Growth Fund" to show the rails holding.

## Who it's for

Community foundations, PTAs and booster clubs with reserves, congregation endowments, small
nonprofit boards, co-op and credit-union investment committees, employer 401(k) committees.
Groups, not individuals — the Good Neighbor audience — and specifically the volunteers who
steward pooled money without staff.

## Why it matters

Most Americans' financed emissions do not live in a personal brokerage account. They live in the
401(k) default fund, the endowment, the reserve — money held in common and decided on by
volunteer committees. Those committees are exactly who gets asked "what's our footprint?" and
exactly who has no way to answer honestly. A confident-but-wrong number (the old public page
implied fossil fuels were 28× clean energy by mixing scopes; like-for-like it is ~9×) does real
damage in a room like that. An agent that produces the number *with* its scope basis, its band,
its unassessed remainder and its sources gives the group a defensible starting point for an
actual decision.

## How we built it

Strands Agents SDK. Six `@tool` functions around a pure, DOM-free model (`src/model.py`) that
is a port of the JavaScript the public calculator ships — and `tests/test_model.py` proves the
two agree through node, so the agent can never quietly disagree with the page. One system prompt
carries the procedure and the honesty rails; `tests/test_judgment_invariants.py` fails if a rail
is dropped. 33 tests, no network. Every saved run ends with a machine check that the brief's numbers are the tool's numbers, computed on exactly the parsed allocation at the real total. Provider is an env switch: OpenRouter (`OpenAIModel` with a
`base_url`) or Amazon Bedrock — same agent either way. `deploy/agentcore_app.py` wraps the agent
for Bedrock AgentCore Runtime.

## Challenges

- **Cash wins every carbon ranking.** At 2 t/$M, "move it to cash" beat every real reallocation.
  It is an exit, not an investment, so the ranker excludes it — a product decision the tests
  now pin.
- **Statements have thousands separators.** "$38,000" was being split at the comma. The parser
  protects them before splitting.
- **The model retyped allocations.** Haiku kept collapsing "VXUS 18%" into 18 points of
  developed markets instead of the parser's 13.5/4.5 split. A prompt rule did not fix it; a
  design change did — the compute tools now take the pasted text verbatim and parse it
  themselves, and the transcript check compares the allocation used to the allocation parsed.
- **Scope mixing.** The single biggest honesty bug in the source page — fossil at Scope 1+2+3
  next to everything else at Scope 1+2 — is fixed at the model layer and the scope basis is a
  required part of every headline the agent writes.

## What's next

Fund-level data (fund fact sheets) behind the same tool surface; live CBECI + market-cap fetch
for the Bitcoin row; a hosted AgentCore endpoint so the calculator page can call the agent
directly.

## Built with

Python · Strands Agents SDK · OpenRouter / Amazon Bedrock · Bedrock AgentCore Runtime · pytest

## Links

- Repo: `<REPO_URL>` (MIT)
- Model UI / live calculator: https://carbon-footprint-calc-wine.vercel.app
- Video: `<VIDEO_URL>`
