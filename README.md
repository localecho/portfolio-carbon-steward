# Portfolio Carbon Steward

> An agent for groups that hold money together and have no analyst. Paste the statement; get a
> five-minute brief on the carbon the pooled money finances, how sure that number is, and which
> single moves would cut it most — with every number traced to a dated source.

Built for the **Agents for Humans Hackathon (AWS) — Good Neighbor Agents** track, on the
[Strands Agents SDK](https://strandsagents.com). The model behind it is the same one that ships
at the public calculator **https://carbon-footprint-calc-wine.vercel.app** (vendored in
`vendor/model.js` and cross-checked by tests).

## Who it's for

A community foundation's volunteer finance committee. A PTA with a reserve fund. A congregation's
endowment committee. A small nonprofit board. A co-op or credit union investment committee. An
employer's 401(k) committee choosing a default fund for sixty people. Groups whose treasurer can
paste a statement but nobody can answer "what is our carbon footprint?" when a donor or a member
asks — and who would be badly served by a number with no scope basis, no uncertainty, and no
sources.

## What it does (end to end, one turn)

1. **Parses what the treasurer actually has** — tickers ("VTI 42%"), dollars ("$38,000 in SPAXX"),
   plain words ("20% international stock fund"), a Vanguard target-date ticker, or a share link
   from the public calculator. Holdings it cannot map are **reported as unassessed with their
   weight, never guessed into a sleeve**.
2. **Computes financed emissions** (tCO2e per year) with a low–high band, on a stated scope basis
   (Scope 1+2 like-for-like by default; an *estimated* Scope 3 view on request).
3. **Puts the number in context** — the same dollars in each Vanguard target-date fund, and the
   average American's personal footprint.
4. **Ranks single reallocation moves** by tonnes saved, carbon-only, never into fossil fuels,
   crypto, or cash — and repeats, every time, that return, risk, fees and fiduciary duty are not
   modeled and belong with the committee's advisor.
5. **Cites** — scope convention, the intensity table, and named, dated sources.

Real, unedited runs: `sample_run_community_foundation.md`, `sample_run_pta_reserve.md`,
`sample_run_congregation_endowment.md` (includes an unmappable holding and a Bitcoin ETF),
`sample_run_share_link_401k.md`.

## Honesty rails (the point of the project)

- The scope basis is in the headline sentence and next to any fossil-vs-clean comparison. On a
  like-for-like basis fossil fuels are **~9×** clean energy, not the 28× the old page implied by
  mixing scopes.
- The band is always shown and always explained (spread of the inputs, not a confidence interval).
- Asset-class averages only. The agent refuses to claim a figure for a specific fund.
- Bitcoin intensity is *derived* (network MtCO2e ÷ market cap, dated inputs) — not a stale lookup.
- "Moving X would cut Y", never "you should move X".
- One turn, no clarifying questions: missing information becomes a stated assumption.
- The model never retypes an allocation. The compute tools take the treasurer's text verbatim and
  parse it deterministically; every saved run carries a machine check that the number was computed
  on exactly what was parsed, at the real total, on the requested scope basis.

## Run it

```bash
uv venv --python 3.12 .venv && uv pip install -r requirements.txt --python .venv/bin/python
export OPENROUTER_API_KEY=...            # default provider; or STEWARD_MODEL_PROVIDER=bedrock
.venv/bin/python -m src.run --profile profiles/community_foundation.yaml
.venv/bin/python -m src.run --text "VTI 60%, BND 30%, cash 10%" --amount 850000 --org "Maple St PTA"
.venv/bin/python -m pytest -q            # 33 tests, no network
```

Provider switch: `STEWARD_MODEL_PROVIDER=openrouter|bedrock`, `STEWARD_MODEL_ID=<id>`. The agent
code is identical either way — Strands handles the provider.

AgentCore: `deploy/agentcore_app.py` wraps the same agent (`agentcore configure --entrypoint
deploy/agentcore_app.py && agentcore launch`). Local: `python deploy/agentcore_app.py` then POST
`{"profile_path": "profiles/pta_reserve.yaml"}` to `:8080/invocations`.

## Architecture

See `ARCHITECTURE.md` (Mermaid). Six Strands tools around a pure, tested model; one system prompt
that encodes the judgment; a YAML profile as the only input.

## Known limitations

- Asset-class averages, not fund-level data. Two funds in the same sleeve get the same intensity.
- Intensities are 2024–2025 estimates and decline ~3–5%/yr as grids decarbonize.
- The Scope 3 view is a rule-of-thumb multiplier, labeled as such.
- The Bitcoin inputs are dated (2026-09-08); the tool exposes them so they can be refreshed.
- Not investment advice. Ever.

## License

MIT.
