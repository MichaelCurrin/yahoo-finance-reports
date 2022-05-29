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

CSV_OUT_CHART_DATA = "out/chart-data.csv"
CSV_OUT_QUOTE_DATA = "out/quote-data.csv"
