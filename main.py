#!/usr/bin/env python
"""
Yahoo Finance Reports application.

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

Data granularity
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
"""
import datetime
import json

import requests

# If the default is not overridden, the API gives a "Forbidden" error.
HEADERS = {"user-agent": "yahoo-finance-reports/0.0.1"}

URL_QUOTE = "https://query1.finance.yahoo.com/v7/finance/quote"
URL_CHART = "https://query1.finance.yahoo.com/v8/finance/chart"

SYMBOLS = ("AAPL", "BYND", "TWOU", "GOOG")
CHART_INTERVAL = "3mo"
CHART_RANGE = "10y"


def request_json(url, params) -> dict:
    resp = requests.get(url, params=params, headers=HEADERS)

    if not resp.ok:
        resp.raise_for_status()

    return resp.json()


def chart_url(symbol: str) -> str:
    """
    Look up time series data for a one stock symbol.

    Unfortunately we can't pick just the fields we want, so get everything.
    """
    return f"{URL_CHART}/{symbol}"


def chart_data(symbol: str, debug: bool = False):
    """
    Lookup chart data for a given symbol.
    """
    url = chart_url(symbol)
    params = dict(interval=CHART_INTERVAL, range=CHART_RANGE)

    resp_data = request_json(url, params)

    if debug:
        print(json.dumps(resp_data, indent=4))
        return

    result = resp_data["chart"]["result"][0]

    meta = result["meta"]
    currency = meta["currency"]
    symbol = meta["symbol"]

    timestamps = result["timestamp"]
    datetimes = [datetime.date.fromtimestamp(ts) for ts in timestamps]
    close_values = result["indicators"]["quote"][0]["close"]

    closes = zip(datetimes, close_values)
    for dt, v in closes:
        print(f"{symbol},{str(dt)},{currency},{v:3.2f}")

    return symbol, currency, closes


def main():
    """
    Command-line entry-point.
    """
    for s in SYMBOLS:
        chart_data(s)


if __name__ == "__main__":
    main()
