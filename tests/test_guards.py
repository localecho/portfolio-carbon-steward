from src.guards import allocation_error
from src.tools.footprint import compute_footprint
from src.tools.shifts import rank_shift_options


def test_fractions_are_rejected_not_silently_computed():
    assert "FRACTIONS" in allocation_error({"us_equities": 0.55, "us_bonds": 0.45}, 1_000_000)
    assert "error" in compute_footprint({"us_equities": 0.55}, 1_000_000)
    assert "error" in rank_shift_options({"us_equities": 0.55}, 1_000_000)


def test_tiny_amount_and_bad_keys_rejected():
    assert "per-$1M" in allocation_error({"us_equities": 100}, 100)
    assert "unknown asset class" in allocation_error({"stocks": 100}, 1_000_000)
    assert allocation_error({}, 1_000_000)


def test_valid_percent_allocation_passes():
    assert allocation_error({"us_equities": 55, "crypto": 3}, 1_150_000) is None
