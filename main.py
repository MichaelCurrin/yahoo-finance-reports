#!/usr/bin/env python
"""
Yahoo Finance Reports application.
"""
import datetime
import json

import requests

# If the default is not overridden, the API gives a "Forbidden" error.
HEADERS = {"user-agent": "yahoo-finance-reports/0.0.1"}


def chart_url(symbol: str) -> str:
    """
    Look up time series data for a given stock symbol.

    Unfortunately we can't pick just the fields we want, so get everything.
    """
    return f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"


def process(url: str, params: dict, debug: bool = False):
    """
    Get and print stock data.
    """
    resp = requests.get(url, params=params, headers=HEADERS)

    if not resp.ok:
        resp.raise_for_status()

    resp_data = resp.json()

    if debug:
        print(json.dumps(resp_data, indent=4))
        return

    result = resp_data["chart"]["result"][0]

    meta = result["meta"]
    currency = meta["currency"]
    symbol = meta["symbol"]
    print(symbol, currency)

    timestamps = result["timestamp"]
    datetimes = [datetime.date.fromtimestamp(ts) for ts in timestamps]
    close_values = result["indicators"]["quote"][0]["close"]

    closes = zip(datetimes, close_values)
    for dt, v in closes:
        print(f"{str(dt)} {v:3.2f}")


def main():
    """
    Command-line entry-point.
    """
    url = chart_url("AAPL")
    params = dict(interval="3mo", range="10y")

    process(url, params)


if __name__ == "__main__":
    main()
