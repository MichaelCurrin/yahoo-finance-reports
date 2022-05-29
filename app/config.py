"""
Valid data granularity intervals
    "1m",
    "2m",
    "5m",
    "15m"
    "30m"
    "90m"
    "1h"
    "1d"
    "5d"
    "1wk"
    "1mo"
    "3mo" quarterly

Valid ranges:
    "1d",
    "5d",
    "1mo",
    "3mo",
    "6mo",
    "1y",
    "2y",
    "5y",
    "10y",
    "ytd",
    "max"
"""
from pathlib import Path

APP_DIR = Path(__file__).parent
OUT_DIR = APP_DIR / "var"
CSV_OUT_CHART_DATA = OUT_DIR / "chart-data.csv"
CSV_OUT_QUOTE_DATA = OUT_DIR / "quote-data.csv"


SYMBOLS = (
    "VOO",
    "QQQ",
    "^RUT",
    "URTH",
    "IWV",
    "VRTTX",
    "STXRAF.JO",
    "SYGEU.JO",
    "AGGE.AS",
    "GC=F",
)

CHART_INTERVAL = "3mo"
CHART_RANGE = "10y"
