from src.model import V
from src.tools.footprint import compute_footprint, reference_points


def test_default_portfolio_matches_public_calculator():
    r = compute_footprint(V["2060 (30)"], 1_000_000)
    assert r["tco2e_per_year"] == 79.3 and r["band_low"] == 63.4 and r["band_high"] == 99.7
    assert r["allocated_pct"] == 100 and r["unallocated_pct"] == 0
    assert r["scope_basis"].startswith("Scope 1+2 (direct")
    assert r["breakdown"][0]["class"] == "us_equities" and r["breakdown"][0]["tco2e_per_year"] == 32.4
    assert r["equivalents"]["passenger_cars"] == 17.2 and r["bitcoin_inputs"] is None


def test_partial_allocation_is_reported_not_normalized():
    r = compute_footprint({"us_equities": 55, "crypto": 3}, 1_150_000)
    assert r["allocated_pct"] == 58 and r["unallocated_pct"] == 42
    assert r["bitcoin_inputs"]["as_of"] == "2026-09-08"


def test_scope3_view_raises_every_number_and_labels_itself():
    a, b = compute_footprint(V["2060 (30)"], 1e6), compute_footprint(V["2060 (30)"], 1e6, scope3=True)
    assert b["tco2e_per_year"] == 158.6 and b["tco2e_per_year"] > a["tco2e_per_year"]
    assert "ESTIMATED" in b["scope_basis"]


def test_reference_points_scale_with_amount():
    r = reference_points(2_400_000)
    assert r["target_date_fund_range_tco2e"] == {"low": 151.44, "high": 190.32, "note": r["target_date_fund_range_tco2e"]["note"]}
    assert r["fossil_vs_clean_lever"] == {"fossil_t_per_musd": 233, "clean_t_per_musd": 25, "ratio": 9.3}


def test_tool_parses_verbatim_text_itself_and_keeps_the_international_split():
    txt = "55% US stock index fund\n20% international stock fund\n20% bond fund\n3% Bitcoin ETF (IBIT)\n2% Legacy Growth Fund"
    r = compute_footprint(None, 1_150_000, True, holdings_text=txt)
    assert r["allocation_used"] == {"us_equities": 55.0, "intl_developed": 15.0, "emerging_markets": 5.0, "us_bonds": 20.0, "crypto": 3.0}
    assert r["parsed"]["unmapped"] == [{"holding": "2% Legacy Growth Fund", "pct": 2.0}] and r["allocated_pct"] == 98
    assert r["tco2e_per_year"] == 154.97


def test_tool_accepts_share_link_and_dollar_text():
    r = compute_footprint(None, None, False, holdings_text="https://carbon-footprint-calc-wine.vercel.app/#a=us_%3A54%2Cint%3A27%2Ceme%3A9%2Cus_b%3A10&$=3200000")
    assert r["amount_usd"] == 3200000 and r["tco2e_per_year"] == 253.76
    r = compute_footprint(None, None, False, holdings_text="$38,000 in SPAXX\n$52,000 in FXAIX\n$10,000 in a savings account")
    assert r["amount_usd"] == 100000 and r["tco2e_per_year"] == 3.22
