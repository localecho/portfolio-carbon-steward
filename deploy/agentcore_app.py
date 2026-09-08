"""Amazon Bedrock AgentCore Runtime entrypoint. Wraps the same Agent built in src/agent.py — a
deployment adapter, not a second implementation.

Local:  python deploy/agentcore_app.py
        curl -X POST http://localhost:8080/invocations -H 'Content-Type: application/json' \
             -d '{"profile_path": "profiles/community_foundation.yaml"}'
AWS:    agentcore configure --entrypoint deploy/agentcore_app.py && agentcore launch
        (set OPENROUTER_API_KEY or STEWARD_MODEL_PROVIDER=bedrock on the runtime)
"""
from __future__ import annotations

import sys
from pathlib import Path

from bedrock_agentcore.runtime import BedrockAgentCoreApp

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.agent import run_for_profile  # noqa: E402
from src.profile import PortfolioProfile  # noqa: E402

app = BedrockAgentCoreApp()


@app.entrypoint
def invoke(payload: dict) -> dict:
    """Accepts {"profile": {...inline fields...}} or {"profile_path": "profiles/x.yaml"}."""
    if "profile" in payload:
        profile = PortfolioProfile(**payload["profile"])
    elif "profile_path" in payload:
        profile = PortfolioProfile.from_yaml(payload["profile_path"])
    else:
        return {"error": "payload must include 'profile' (inline fields) or 'profile_path' (YAML path)."}
    return {"org": profile.name, "brief": run_for_profile(profile)}


if __name__ == "__main__":
    app.run()
