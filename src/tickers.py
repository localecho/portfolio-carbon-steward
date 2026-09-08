"""Maps what a volunteer actually pastes from a statement — tickers and plain words — onto the
nine asset-class sleeves. This is ALLOCATION mapping only: no carbon number is ever attached to a
specific fund. Anything not in this table is reported back as unmapped, never guessed."""
from __future__ import annotations

# ticker -> sleeve key, or a split dict, or ("preset", key) for target-date funds
TICKERS: dict[str, object] = {
    # US total market / S&P 500
    "VTI": "us_equities", "VOO": "us_equities", "SPY": "us_equities", "IVV": "us_equities",
    "VFIAX": "us_equities", "FXAIX": "us_equities", "VTSAX": "us_equities", "SWPPX": "us_equities",
    "FSKAX": "us_equities", "SCHB": "us_equities", "ITOT": "us_equities", "QQQ": "us_equities",
    # International total (developed + emerging, split like the calculator's glide-path proxy)
    "VXUS": {"intl_developed": 0.75, "emerging_markets": 0.25},
    "VTIAX": {"intl_developed": 0.75, "emerging_markets": 0.25},
    "IXUS": {"intl_developed": 0.75, "emerging_markets": 0.25},
    "FTIHX": {"intl_developed": 0.75, "emerging_markets": 0.25},
    # Developed / emerging
    "VEA": "intl_developed", "IEFA": "intl_developed", "EFA": "intl_developed", "VTMGX": "intl_developed", "SCHF": "intl_developed",
    "VWO": "emerging_markets", "IEMG": "emerging_markets", "EEM": "emerging_markets", "VEMAX": "emerging_markets", "SCHE": "emerging_markets",
    # Bonds
    "BND": "us_bonds", "AGG": "us_bonds", "BNDX": "us_bonds", "VBTLX": "us_bonds", "FXNAX": "us_bonds",
    "VGIT": "us_bonds", "VGSH": "us_bonds", "TLT": "us_bonds", "SCHZ": "us_bonds", "VCIT": "us_bonds", "LQD": "us_bonds",
    # Real estate
    "VNQ": "real_estate", "SCHH": "real_estate", "VGSLX": "real_estate", "IYR": "real_estate", "XLRE": "real_estate",
    # Fossil-fuel sector funds
    "XLE": "fossil_fuels", "VDE": "fossil_fuels", "IYE": "fossil_fuels", "FENY": "fossil_fuels", "XOP": "fossil_fuels", "OIH": "fossil_fuels",
    # Clean energy
    "ICLN": "clean_energy", "QCLN": "clean_energy", "TAN": "clean_energy", "PBW": "clean_energy", "FAN": "clean_energy",
    # Cash / money market
    "VMFXX": "cash", "SPAXX": "cash", "FDRXX": "cash", "SWVXX": "cash", "BIL": "cash", "SGOV": "cash",
    # Bitcoin exposure
    "IBIT": "crypto", "FBTC": "crypto", "GBTC": "crypto", "BITB": "crypto", "ARKB": "crypto",
    # Vanguard Target Retirement funds -> calculator presets
    "VSVNX": ("preset", "2070 (20)"), "VLXVX": ("preset", "2060 (30)"), "VTTSX": ("preset", "2060 (30)"),
    "VFFVX": ("preset", "2050 (40)"), "VFIFX": ("preset", "2050 (40)"), "VTIVX": ("preset", "2045 (45)"),
    "VFORX": ("preset", "2040 (50)"), "VTTHX": ("preset", "2035 (55)"), "VTHRX": ("preset", "2030 (60)"),
    "VTTVX": ("preset", "2025 (65)"), "VTINX": ("preset", "Income (72)"),
}

# plain-language phrases -> sleeve (matched case-insensitively, longest phrase first)
PHRASES: list[tuple[str, object]] = [
    ("target date 2070", ("preset", "2070 (20)")), ("target date 2065", ("preset", "2060 (30)")),
    ("target date 2060", ("preset", "2060 (30)")), ("target date 2055", ("preset", "2050 (40)")),
    ("target date 2050", ("preset", "2050 (40)")), ("target date 2045", ("preset", "2045 (45)")),
    ("target date 2040", ("preset", "2040 (50)")), ("target date 2035", ("preset", "2035 (55)")),
    ("target date 2030", ("preset", "2030 (60)")), ("target date 2025", ("preset", "2025 (65)")),
    ("target retirement income", ("preset", "Income (72)")),
    ("international developed", "intl_developed"), ("developed markets", "intl_developed"), ("eafe", "intl_developed"),
    ("emerging markets", "emerging_markets"), ("emerging market", "emerging_markets"),
    ("international stock", {"intl_developed": 0.75, "emerging_markets": 0.25}),
    ("international equit", {"intl_developed": 0.75, "emerging_markets": 0.25}),
    ("total international", {"intl_developed": 0.75, "emerging_markets": 0.25}),
    ("foreign stock", {"intl_developed": 0.75, "emerging_markets": 0.25}),
    ("s&p 500", "us_equities"), ("total stock market", "us_equities"), ("us stock", "us_equities"), ("u.s. stock", "us_equities"),
    ("us equit", "us_equities"), ("u.s. equit", "us_equities"), ("domestic stock", "us_equities"), ("domestic equit", "us_equities"),
    ("large cap", "us_equities"), ("index fund", "us_equities"),
    ("fixed income", "us_bonds"), ("treasur", "us_bonds"), ("bond", "us_bonds"),
    ("real estate", "real_estate"), ("reit", "real_estate"),
    ("fossil", "fossil_fuels"), ("oil & gas", "fossil_fuels"), ("oil and gas", "fossil_fuels"), ("energy sector", "fossil_fuels"),
    ("clean energy", "clean_energy"), ("renewable", "clean_energy"), ("solar", "clean_energy"), ("wind energy", "clean_energy"),
    ("money market", "cash"), ("cash", "cash"), ("certificate of deposit", "cash"), ("savings account", "cash"), ("cd ladder", "cash"),
    ("bitcoin", "crypto"), ("crypto", "crypto"), ("btc", "crypto"),
]
