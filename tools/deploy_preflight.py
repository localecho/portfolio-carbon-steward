"""AWS AgentCore deploy-readiness preflight for Portfolio Carbon Steward.

Run once AWS credentials are configured, before `agentcore configure && agentcore launch`.
Checks the things that would otherwise fail *during* a deploy attempt -- same idea as this
repo's hackathon-submission preflight pattern: catch a real gap here, in seconds, not mid-launch.

Usage:
    python tools/deploy_preflight.py
"""
from __future__ import annotations

import json
import os
import subprocess
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class CheckResult:
    name: str
    passed: bool
    detail: str
    fix: str = ""


@dataclass
class Summary:
    results: list[CheckResult] = field(default_factory=list)

    @property
    def fail_count(self) -> int:
        return sum(1 for r in self.results if not r.passed)

    @property
    def safe_to_deploy(self) -> bool:
        return self.fail_count == 0

    @property
    def next_steps(self) -> str:
        fixes = [r.fix for r in self.results if not r.passed and r.fix]
        return "\n".join(f"  - {f}" for f in fixes)


def check_aws_cli(runner=subprocess.run) -> CheckResult:
    r = runner(["aws", "--version"], capture_output=True, text=True)
    if r.returncode == 0:
        return CheckResult("AWS CLI installed", True, r.stdout.strip() or r.stderr.strip())
    return CheckResult(
        "AWS CLI installed", False, "aws command not found",
        fix="brew install awscli",
    )


def check_aws_credentials(runner=subprocess.run) -> CheckResult:
    r = runner(
        ["aws", "sts", "get-caller-identity", "--output", "json"],
        capture_output=True, text=True,
    )
    if r.returncode == 0:
        try:
            identity = json.loads(r.stdout)
            account = identity.get("Account", "unknown")
        except (json.JSONDecodeError, AttributeError):
            account = "unknown"
        return CheckResult("AWS credentials configured", True, f"account {account}")
    return CheckResult(
        "AWS credentials configured", False,
        (r.stderr or "no credentials found").strip(),
        fix='aws configure   # paste your Access Key ID + Secret + region (us-east-1)',
    )


def check_agentcore_cli(runner=subprocess.run) -> CheckResult:
    # Typer-based CLI: no --version flag (returns exit 2, "No such option"). --help is the
    # reliable "is this installed and runnable" probe -- found live after --version silently
    # false-failed a working install.
    r = runner(["agentcore", "--help"], capture_output=True, text=True)
    if r.returncode == 0:
        return CheckResult("agentcore CLI installed", True, "agentcore --help exits 0")
    return CheckResult(
        "agentcore CLI installed", False, "agentcore command not found",
        fix="pip install bedrock-agentcore-starter-toolkit",
    )


def check_openrouter_key() -> CheckResult:
    if os.environ.get("OPENROUTER_API_KEY"):
        return CheckResult("OPENROUTER_API_KEY set", True, "present in environment")
    return CheckResult(
        "OPENROUTER_API_KEY set", False, "not set in environment",
        fix="export OPENROUTER_API_KEY=... (same key used for local runs)",
    )


def check_deploy_adapter_imports() -> CheckResult:
    adapter = Path(__file__).resolve().parent.parent / "deploy" / "agentcore_app.py"
    if not adapter.exists():
        return CheckResult("deploy/agentcore_app.py present", False, "file missing", fix="restore deploy/agentcore_app.py")
    try:
        import ast

        ast.parse(adapter.read_text())
    except SyntaxError as exc:
        return CheckResult("deploy/agentcore_app.py present", False, f"syntax error: {exc}")
    return CheckResult("deploy/agentcore_app.py present", True, str(adapter))


def run_all_checks(checks: list[CheckResult] | None = None) -> Summary:
    if checks is None:
        checks = [
            check_aws_cli(),
            check_aws_credentials(),
            check_agentcore_cli(),
            check_openrouter_key(),
            check_deploy_adapter_imports(),
        ]
    return Summary(results=checks)


def main() -> None:
    summary = run_all_checks()
    for r in summary.results:
        mark = "PASS" if r.passed else "FAIL"
        print(f"{mark}  {r.name} -- {r.detail}")

    print()
    if summary.safe_to_deploy:
        print("SAFE TO DEPLOY. Next:")
        print("  agentcore configure --entrypoint deploy/agentcore_app.py")
        print("  agentcore launch")
    else:
        print(f"{summary.fail_count} FAIL -- fix before deploying:")
        print(summary.next_steps)


if __name__ == "__main__":
    main()
