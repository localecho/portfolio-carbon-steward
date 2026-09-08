from src.tools.shifts import CARBON_ONLY_NOTE, rank_shift_options


ALLOC = {"us_equities": 42, "intl_developed": 13.5, "emerging_markets": 4.5, "us_bonds": 25, "real_estate": 5, "fossil_fuels": 4, "cash": 6}


def test_never_proposes_fossil_crypto_or_cash_as_destination():
    r = rank_shift_options(ALLOC, 2_400_000)
    assert all(o["to"] not in ("fossil_fuels", "crypto", "cash") for o in r["options"])
    assert r["never_proposed_as_destination"][:2] == ["fossil_fuels", "crypto"]


def test_options_sorted_desc_and_capped_by_holding():
    r = rank_shift_options(ALLOC, 2_400_000, max_points=10)
    saved = [o["tco2e_saved_per_year"] for o in r["options"]]
    assert saved == sorted(saved, reverse=True)
    fossil = [o for o in r["options"] if o["from"] == "fossil_fuels"]
    assert fossil and fossil[0]["move_points"] == 4 and fossil[0]["capped_by_holding"] is True
    # 4 points of $2.4M from 233 → 25: 0.04 × 2.4 × 208 = 19.97
    assert fossil[0]["to"] == "clean_energy" and fossil[0]["tco2e_saved_per_year"] == 19.97


def test_top_option_is_the_largest_high_intensity_sleeve_not_fossil_when_fossil_is_tiny():
    r = rank_shift_options(ALLOC, 2_400_000, max_points=10)
    top = r["options"][0]
    # 10 points of US equities (60→25) saves 0.10×2.4×35 = 8.4; EM 4.5 points (190→25) saves 0.045×2.4×165 = 17.82;
    # fossil 4 points saves 19.97 → fossil first, then EM, then US equities
    assert (top["from"], top["to"]) == ("fossil_fuels", "clean_energy")
    assert (r["options"][1]["from"], r["options"][1]["tco2e_saved_per_year"]) == ("emerging_markets", 17.82)


def test_disclaimer_present_and_single_sleeve_portfolio_still_gets_options():
    r = rank_shift_options({"us_equities": 100}, 1e6, max_points=10)
    assert r["options"] and r["options"][0]["to"] == "clean_energy" and r["options"][0]["tco2e_saved_per_year"] == 3.5
    assert r["note"] == CARBON_ONLY_NOTE and "fiduciary" in r["note"]


def test_baseline_equals_footprint_and_new_total_is_consistent():
    r = rank_shift_options(ALLOC, 2_400_000)
    o = r["options"][0]
    assert round(r["baseline_tco2e"] - o["tco2e_saved_per_year"], 1) == round(o["new_total_tco2e"], 1)


def test_rank_shifts_from_verbatim_text_matches_dict_path():
    txt = "VTI 42%\nVXUS 18%\nBND 25%\nVNQ 5%\nXLE 4%\nLocal bank CD ladder 6%"
    a = rank_shift_options(None, 2_400_000, holdings_text=txt)
    b = rank_shift_options(ALLOC, 2_400_000)
    assert a["allocation_used"] == b["allocation_used"] and a["options"] == b["options"]
