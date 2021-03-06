"""
Yahoo API module.
"""
import datetime
import sys
from typing import List

import requests

from . import lib
from .config import CHART_INTERVAL, CHART_RANGE

# If the default is not overridden, the API gives a "Forbidden" error.
HEADERS = {"user-agent": "github.com/MichaelCurrin/yahoo-finance-reports"}

URL_QUOTE = "https://query1.finance.yahoo.com/v7/finance/quote"
URL_CHART = "https://query1.finance.yahoo.com/v8/finance/chart"

SOUTH_AFRICAN_RANDS_CENTS = "ZAc"
SOUTH_AFRICAN_RANDS = "ZAR"


def request_json(symbol_description: str, url: str, params: dict) -> dict:
    """
    Request given URL with parameters and return response data.
    """
    resp = requests.get(url, params=params, headers=HEADERS)

    print("For symbols:", symbol_description)
    print("Requesting URL", resp.url)

    resp_json = resp.json()

    if not resp.ok:
        lib.print_error(f"Failed to request URL. Reason - {resp.reason}")

        if resp_json["chart"]:
            error = resp_json["chart"]["error"]
        else:
            error = resp_json["quote"]["error"]
        print(f"Code: {error['code']}. Description: {error['description']}")

        sys.exit(1)

    return resp_json


def chart_url(symbol: str) -> str:
    """
    Look up time series data for a one stock symbol.

    Unfortunately we can't pick just the fields we want, so get everything.
    """
    return f"{URL_CHART}/{symbol}"


def format_quote(value: dict) -> dict:
    """
    Get relevant data from a quote.

    Rands are in cents so need to be converted to Rands. Short name can have
    spaces or invisible characters which need to be stripped out.
    """
    currency = value["currency"]
    price = value["regularMarketPrice"]
    low52 = value["fiftyTwoWeekLow"]
    high52 = value["fiftyTwoWeekHigh"]

    if currency == SOUTH_AFRICAN_RANDS_CENTS:
        currency = SOUTH_AFRICAN_RANDS
        price = price / 100
        low52 = low52 / 100
        high52 = high52 / 100

    return dict(
        symbol=value["symbol"],
        short_name=value["shortName"].strip(),
        long_name=value.get("longName", ""),
        type_disp=value["typeDisp"],
        currency=currency,
        quote_type=value["quoteType"],
        price=price,
        low52=low52,
        high52=high52,
        region=value["region"],
    )


def get_chart_data(symbol: str, debug: bool = False):
    """
    Lookup chart data for a given symbol.

    TODO: Open might be better since the date is the first day of the quarter.
    """
    url = chart_url(symbol)
    params = dict(interval=CHART_INTERVAL, range=CHART_RANGE)

    resp_data = request_json(symbol, url, params)

    if debug:
        lib.print_debug(resp_data)

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


def get_quote_data(symbols: List[str], debug: bool = False):
    """
    Lookup latest quote data for given symbols.
    """
    url = URL_QUOTE
    params = dict(symbols=symbols)

    resp_data = request_json(str(symbols), url, params)

    if debug:
        lib.print_debug(resp_data)

    result = resp_data["quoteResponse"]["result"]

    return [format_quote(x) for x in result]
