"""The Python port must match the vendored JS model the public calculator ships — checked through
node against vendor/model.js, not by eyeballing constants."""
import json, shutil, subprocess
from pathlib import Path

import pytest

from src import model as M

ROOT = Path(__file__).resolve().parents[1]
r1 = lambda x: round(x, 1)


@pytest.mark.skipif(shutil.which("node") is None, reason="node not installed")
def test_python_table_matches_vendored_js():
    js = json.loads(subprocess.check_output(
        ["node", "-e", "const M=require(process.argv[1]);console.log(JSON.stringify({C:M.C,V:M.V,pr:M.presetRange(false),lv:[M.leverRatio(false),M.leverRatio(true)]}))",
         str(ROOT / "vendor/model.js")], text=True))
    assert set(js["C"]) == set(M.C)
    for k, d in js["C"].items():
        for f in ("t", "lo", "hi", "s3"):
            assert r1(d[f]) == r1(M.C[k][f]), (k, f)
    assert js["V"] == {k: {kk: vv for kk, vv in v.items()} for k, v in M.V.items()}
    pr = M.preset_range()
    assert r1(js["pr"]["min"]) == r1(pr["min"]) and r1(js["pr"]["max"]) == r1(pr["max"])
    assert [round(x) for x in js["lv"]] == [round(M.lever_ratio(False)), round(M.lever_ratio(True))]


def test_default_target_date_portfolio_is_79_3():
    assert r1(M.em(M.V["2060 (30)"], 1)) == 79.3


def test_scope_basis_and_lever():
    assert M.C["fossil_fuels"]["t"] == 233 and M.intensity("fossil_fuels", True) == 699
    assert round(M.lever_ratio(False)) == 9 and round(M.lever_ratio(True)) == 14
    assert "ESTIMATED" in M.ScopeBasis(True).label and "same basis" in M.ScopeBasis(False).label


def test_bitcoin_is_derived_and_refreshable():
    assert r1(M.crypto_intensity(39.8, 1.578e12)) == 25.2
    t = M.table(btc_mt=39.8, btc_cap_usd=1.578e12 / 2)
    assert r1(t["crypto"]["t"]) == 50.4          # price halves → intensity doubles
    assert M.C["crypto"]["t"] != t["crypto"]["t"]  # table() never mutates the module default


def test_band_and_preset_range():
    b = M.band(M.V["2060 (30)"], 1)
    assert r1(b["lo"]) == 63.4 and r1(b["hi"]) == 99.7 and b["lo"] < b["t"] < b["hi"]
    pr = M.preset_range()
    assert (r1(pr["min"]), r1(pr["max"])) == (63.1, 79.3)
