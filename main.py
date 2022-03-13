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
import csv
import datetime
import json
from typing import List

import requests

# If the default is not overridden, the API gives a "Forbidden" error.
HEADERS = {"user-agent": "yahoo-finance-reports/0.0.1"}

URL_CHART = "https://query1.finance.yahoo.com/v8/finance/chart"

SYMBOLS = ("MTN.JO", "SYGESG.JO", "AAPL", "BYND", "TWOU", "GOOG")

CHART_INTERVAL = "3mo"
CHART_RANGE = "10y"

CSV_OUT_CHART_DATA = "chart-data.csv"


def request_json(url, params) -> dict:
    resp = requests.get(url, params=params, headers=HEADERS)

    if not resp.ok:
        resp.raise_for_status()

    return resp.json()


def write_csv(path: str, out_data: List[dict], field_names: List[str]) -> None:
    with open(path, "w", encoding="utf-8") as f_out:
        writer = csv.DictWriter(f_out, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(out_data)


def chart_url(symbol: str) -> str:
    """
    Look up time series data for a one stock symbol.

    Unfortunately we can't pick just the fields we want, so get everything.
    """
    return f"{URL_CHART}/{symbol}"


def get_chart_data(symbol: str, debug: bool = False):
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

    if currency == "ZAc":
        currency = "ZAR"
        close_values = [x / 100 for x in close_values]

    closes = zip(datetimes, close_values)

    return [
        dict(datetime=x[0], symbol=symbol, currency=currency, price=round(x[1], 2))
        for x in closes
    ]


def process_chart_data():
    chart_data = [get_chart_data(s) for s in SYMBOLS]
    flat_chart_data = [x for group in chart_data for x in group]
    field_names = list(flat_chart_data[0].keys())

    write_csv(CSV_OUT_CHART_DATA, flat_chart_data, field_names)


def main():
    """
    Command-line entry-point.
    """
    process_chart_data()


if __name__ == "__main__":
    main()
