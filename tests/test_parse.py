from src.tools.parse import parse_holdings_text, parse_share_link_str


def test_ticker_percent_list_maps_and_splits_international():
    r = parse_holdings_text("VTI 42%\nVXUS 18%\nBND 25%\nVNQ 5%\nXLE 4%\nLocal bank CD ladder 6%")
    a = r["allocation"]
    assert a["us_equities"] == 42 and a["us_bonds"] == 25 and a["real_estate"] == 5 and a["fossil_fuels"] == 4
    assert a["intl_developed"] == 13.5 and a["emerging_markets"] == 4.5   # 18 × 75/25
    assert a["cash"] == 6 and r["unmapped"] == [] and r["mapped_pct"] == 100


def test_dollar_statement_derives_weights_and_total():
    r = parse_holdings_text("$38,000 in a Fidelity money market (SPAXX)\n$52,000 in FXAIX\n$10,000 in a credit union savings account")
    assert r["amount_usd"] == 100000
    assert r["allocation"] == {"cash": 48.0, "us_equities": 52.0}
    assert r["unmapped"] == []


def test_unknown_fund_is_reported_not_guessed():
    r = parse_holdings_text('55% US stock index fund, 20% international stock fund, 20% bond fund, 3% Bitcoin ETF (IBIT), 2% "Legacy Growth Fund" (details unknown)')
    assert r["unmapped"] == [{"holding": '2% "Legacy Growth Fund" (details unknown)', "pct": 2.0}]
    assert r["unmapped_pct"] == 2.0 and r["mapped_pct"] == 98.0
    assert r["allocation"]["crypto"] == 3 and r["allocation"]["us_equities"] == 55
    assert "unassessed" in r["note"]


def test_target_date_ticker_expands_to_glide_path():
    r = parse_holdings_text("VFIFX 100%")
    assert r["allocation"] == {"us_equities": 54.0, "intl_developed": 27.0, "emerging_markets": 9.0, "us_bonds": 10.0}


def test_empty_or_numberless_text():
    r = parse_holdings_text("we hold some index funds and a bit of cash")
    assert r["allocation"] == {} and "needs a % or a $" in r["note"]


def test_share_link_roundtrip_including_scope():
    r = parse_share_link_str("https://carbon-footprint-calc-wine.vercel.app/#a=us_%3A54%2Cint%3A27%2Ceme%3A9%2Cus_b%3A10&$=3200000&s=3")
    assert r["valid"] and r["amount_usd"] == 3200000 and r["scope3"] is True
    assert r["allocation"] == {"us_equities": 54, "intl_developed": 27, "emerging_markets": 9, "us_bonds": 10}
    assert parse_share_link_str("https://example.com/#nothing")["valid"] is False
