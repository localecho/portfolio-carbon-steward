"""TDD for the AWS AgentCore deploy-readiness preflight (tools/deploy_preflight.py).

Written before the implementation, same pattern as Continuity Check's tools/preflight.sh:
a real pre-deploy check the operator runs once AWS credentials exist, so "agentcore launch"
never fails halfway through for a reason this script could have caught first.
"""
from __future__ import annotations

from tools.deploy_preflight import (
    CheckResult,
    check_agentcore_cli,
    check_aws_cli,
    check_aws_credentials,
    check_deploy_adapter_imports,
    check_openrouter_key,
    run_all_checks,
)


class FakeRunner:
    """Stand-in for subprocess.run -- records calls, returns scripted results."""

    def __init__(self, results: dict[str, tuple[int, str, str]]):
        self.results = results
        self.calls: list[list[str]] = []

    def __call__(self, cmd, **kwargs):
        self.calls.append(cmd)
        key = cmd[0]
        code, out, err = self.results.get(key, (127, "", f"{key}: not found"))

        class R:
            returncode = code
            stdout = out
            stderr = err

        return R()


def test_check_aws_cli_passes_when_aws_binary_found():
    runner = FakeRunner({"aws": (0, "aws-cli/2.36.42 Python/3.14.7 Darwin/25.6.0", "")})
    result = check_aws_cli(runner=runner)
    assert result.passed is True
    assert "2.36.42" in result.detail


def test_check_aws_cli_fails_when_aws_not_installed():
    runner = FakeRunner({})
    result = check_aws_cli(runner=runner)
    assert result.passed is False
    assert "brew install awscli" in result.fix


def test_check_aws_credentials_passes_with_valid_identity():
    runner = FakeRunner(
        {"aws": (0, '{"Account": "123456789012", "Arn": "arn:aws:iam::123456789012:user/x"}', "")}
    )
    result = check_aws_credentials(runner=runner)
    assert result.passed is True
    assert "123456789012" in result.detail


def test_check_aws_credentials_fails_with_clear_fix_when_unconfigured():
    runner = FakeRunner(
        {"aws": (1, "", "Unable to locate credentials. You can configure credentials by running \"aws configure\".")}
    )
    result = check_aws_credentials(runner=runner)
    assert result.passed is False
    assert "aws configure" in result.fix


def test_check_agentcore_cli_passes_when_installed():
    # Real behavior, found live: agentcore is Typer-based and has no --version flag (exits 2,
    # "No such option") -- --help is the actual "is this installed" probe.
    runner = FakeRunner({"agentcore": (0, "Usage: agentcore [OPTIONS] COMMAND [ARGS]...", "")})
    result = check_agentcore_cli(runner=runner)
    assert result.passed is True


def test_check_agentcore_cli_fails_with_pip_install_fix():
    runner = FakeRunner({})
    result = check_agentcore_cli(runner=runner)
    assert result.passed is False
    assert "bedrock-agentcore-starter-toolkit" in result.fix


def test_check_openrouter_key_passes_when_set(monkeypatch):
    monkeypatch.setenv("OPENROUTER_API_KEY", "sk-or-v1-fake-for-test")
    result = check_openrouter_key()
    assert result.passed is True


def test_check_openrouter_key_fails_when_unset(monkeypatch):
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    result = check_openrouter_key()
    assert result.passed is False
    assert "OPENROUTER_API_KEY" in result.fix


def test_check_deploy_adapter_imports_passes_for_real_file():
    result = check_deploy_adapter_imports()
    assert result.passed is True


def test_run_all_checks_reports_safe_to_deploy_only_when_everything_passes():
    all_pass = [CheckResult("a", True, "ok", "")] * 3
    summary = run_all_checks(checks=all_pass)
    assert summary.safe_to_deploy is True
    assert summary.fail_count == 0

    one_fail = [CheckResult("a", True, "ok", ""), CheckResult("b", False, "bad", "fix b")]
    summary = run_all_checks(checks=one_fail)
    assert summary.safe_to_deploy is False
    assert summary.fail_count == 1
    assert "fix b" in summary.next_steps
