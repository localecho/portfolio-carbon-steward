"""The rails live in the system prompt and the tool surface; these tests make sure a refactor
can't quietly drop one. Builds the real Agent with a fake key — no network call is made."""
import os
from unittest.mock import patch

from src.agent import SYSTEM_PROMPT, TOOLS, build_agent
from src.profile import PortfolioProfile


def test_system_prompt_carries_every_rail():
    for phrase in ("scope basis", "low–high band", "asset-class averages", "carbon-only", "fossil fuels, crypto, or cash",
                   "never stop to ask", "Unassessed", "at most 3", "Do not add outside carbon statistics", "COPIED VERBATIM", "NEVER retype an allocation"):
        assert phrase in SYSTEM_PROMPT, phrase


def test_tool_surface_is_exactly_the_six_documented_tools():
    names = sorted(t.tool_name for t in TOOLS)
    assert names == sorted(["parse_allocation", "parse_share_link", "calculate_financed_emissions", "compare_to_reference", "rank_shifts", "data_provenance"])


@patch.dict(os.environ, {"OPENROUTER_API_KEY": "test-key-not-real", "STEWARD_MODEL_PROVIDER": "openrouter"})
def test_agent_builds_with_openrouter_provider_offline():
    agent = build_agent()
    assert len(agent.tool_names) == 6 and "rank_shifts" in agent.tool_names


def test_profile_prompt_block_states_scope_and_limit():
    p = PortfolioProfile.from_yaml("profiles/congregation_endowment.yaml")
    block = p.as_prompt_block()
    assert "Scope 1+2 + estimated Scope 3" in block and "10 points" in block and "Legacy Growth Fund" in block
    for f in ("community_foundation", "pta_reserve", "share_link_401k_committee"):
        PortfolioProfile.from_yaml(f"profiles/{f}.yaml")
