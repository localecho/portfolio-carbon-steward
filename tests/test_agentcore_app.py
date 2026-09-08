from unittest.mock import patch

from deploy.agentcore_app import invoke


@patch("deploy.agentcore_app.run_for_profile", return_value="mocked brief")
def test_invoke_with_profile_path(mock_run):
    r = invoke({"profile_path": "profiles/pta_reserve.yaml"})
    assert r == {"org": "Lincoln Elementary PTA Reserve Fund", "brief": "mocked brief"}
    mock_run.assert_called_once()


@patch("deploy.agentcore_app.run_for_profile", return_value="mocked brief")
def test_invoke_inline(mock_run):
    r = invoke({"profile": {"name": "X", "org_type": "PTA", "holdings_text": "VTI 100%", "amount_usd": 1000}})
    assert r["org"] == "X"


def test_invoke_bad_payload():
    assert "error" in invoke({"nope": 1})
