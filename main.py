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

from config import (
    CHART_INTERVAL,
    CHART_RANGE,
    CSV_OUT_CHART_DATA,
    CSV_OUT_QUOTE_DATA,
    SYMBOLS,
)

# If the default is not overridden, the API gives a "Forbidden" error.
HEADERS = {"user-agent": "github.com/MichaelCurrin/yahoo-finance-reports"}

URL_QUOTE = "https://query1.finance.yahoo.com/v7/finance/quote"
URL_CHART = "https://query1.finance.yahoo.com/v8/finance/chart"


def request_json(url, params) -> dict:
    resp = requests.get(url, params=params, headers=HEADERS)

    print("Requesting", resp.url)

    if not resp.ok:
        resp.raise_for_status()

    return resp.json()


def write_csv(path: str, out_data: List[dict], field_names: List[str]) -> None:
    with open(path, "w", encoding="utf-8") as f_out:
        writer = csv.DictWriter(f_out, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(out_data)


def print_debug(value) -> None:
    print(json.dumps(value, indent=4))


def chart_url(symbol: str) -> str:
    """
    Look up time series data for a one stock symbol.

    Unfortunately we can't pick just the fields we want, so get everything.
    """
    return f"{URL_CHART}/{symbol}"


def format_quote(value):
    currency = value["currency"]
    price = value["regularMarketPrice"]
    low52 = value["fiftyTwoWeekLow"]
    high52 = value["fiftyTwoWeekHigh"]

    if currency == "ZAc":
        currency = "ZAR"
        price = price / 100
        low52 = low52 / 100
        high52 = high52 / 100

    return dict(
        symbol=value["symbol"],
        short_name=value["shortName"],
        long_name=value["longName"],
        type=value["typeDisp"],
        currency=currency,
        price=price,
    )


def get_quote_data(symbols: List[str], debug: bool = False):
    """
    Lookup latest quote data for given symbols.
    """
    url = URL_QUOTE
    params = dict(symbols=symbols)

    resp_data = request_json(url, params)

    if debug:
        print_debug(resp_data)

    result = resp_data["quoteResponse"]["result"]

    return [format_quote(x) for x in result]


def get_chart_data(symbol: str, debug: bool = False):
    """
    Lookup chart data for a given symbol.
    """
    url = chart_url(symbol)
    params = dict(interval=CHART_INTERVAL, range=CHART_RANGE)

    resp_data = request_json(url, params)

    if debug:
        print_debug(resp_data)

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


def process_quote_data():
    quote_data = get_quote_data(",".join(SYMBOLS))

    field_names = list(quote_data[0].keys())
    write_csv(CSV_OUT_QUOTE_DATA, quote_data, field_names)


def process_chart_data():
    chart_data = [get_chart_data(s) for s in SYMBOLS]
    flat_chart_data = [x for group in chart_data for x in group]
    field_names = list(flat_chart_data[0].keys())

    write_csv(CSV_OUT_CHART_DATA, flat_chart_data, field_names)


def main():
    """
    Command-line entry-point.
    """
    process_quote_data()
    process_chart_data()


if __name__ == "__main__":
    main()
