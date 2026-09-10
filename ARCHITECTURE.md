# Architecture

```mermaid
flowchart LR
    subgraph Input["What the committee gives (once)"]
        P[profiles/*.yaml<br/>name · org type · holdings text or share link · amount · scope · max move]
    end

    subgraph Agent["Strands Agent (src/agent.py)"]
        SP[System prompt<br/>procedure + honesty rails]
        M[(Model provider<br/>OpenRouter → claude-haiku-4.5<br/>or Amazon Bedrock)]
    end

    subgraph Tools["Six @tool functions (src/tools/)"]
        T1[parse_allocation<br/>tickers · dollars · phrases · TDF tickers<br/>unmapped → reported, never guessed]
        T2[parse_share_link<br/>decodes the public calculator's #hash]
        T3[calculate_financed_emissions<br/>takes the text VERBATIM, parses it itself<br/>E = Σ w·A·I · low–high band · scope basis]
        T4[compare_to_reference<br/>target-date range · avg American · lever ratio]
        T5[rank_shifts<br/>same verbatim text · carbon-only<br/>never → fossil/crypto/cash]
        T6[data_provenance<br/>table · scope convention · dated sources]
    end

    subgraph Model["Pure model (src/model.py)"]
        C[Intensity table<br/>9 sleeves · Scope 1+2 · s3 multipliers]
        B[Bitcoin row DERIVED<br/>MtCO2e ÷ market cap]
        V[Vanguard glide-path presets]
    end

    JS[vendor/model.js<br/>same model the public calculator ships] -. cross-checked by tests/test_model.py .-> Model

    P --> Agent
    SP --> M
    M <--> T1 & T2 & T3 & T4 & T5 & T6
    T1 & T2 -.-> T3
    T3 & T4 & T5 & T6 --> Model
    M --> OUT[Markdown brief<br/>headline · meaning · breakdown · unassessed · ≤3 options · how sure]

    subgraph Deploy
        CLI[src/run.py CLI]
        AC[deploy/agentcore_app.py<br/>Bedrock AgentCore Runtime entrypoint]
    end
    CLI --> Agent
    AC --> Agent
```

**Why the model is separate from the tools.** `src/model.py` has no Strands import and no I/O; the
tools are thin, typed wrappers with docstrings the model reads. That keeps the arithmetic testable
without a model call (36 tests, ~1 s, no network) and lets `tests/test_model.py` prove the Python
port matches the JavaScript the public calculator serves — the agent can never quietly disagree
with the page.

**Why six tools, not one.** Each tool is a claim the brief has to make separately: what was parsed
(and what wasn't), the number and its band, the context, the options, the sources. Separate tool
results are what the honesty rails ground against — "ground every number in a tool result" only
works if the tool results are legible.

**Provider.** `STEWARD_MODEL_PROVIDER=openrouter` (default) uses Strands' `OpenAIModel` with
`base_url` pointed at OpenRouter; `bedrock` uses `BedrockModel`. Same agent, same prompt, same
tools.
