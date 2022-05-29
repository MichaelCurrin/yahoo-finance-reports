"""
Yahoo Finance Reports application.
"""
from typing import List

from . import api, lib
from .config import CSV_OUT_CHART_DATA, CSV_OUT_QUOTE_DATA, SYMBOLS


def process_chart_data():
    """
    Write fetched chart data as a CSV.
    """
    chart_data_by_symbol = [api.get_chart_data(s) for s in SYMBOLS]
    flat_chart_data = [x for group in chart_data_by_symbol for x in group]
    field_names = list(flat_chart_data[0].keys())

    lib.write_csv(CSV_OUT_CHART_DATA, flat_chart_data, field_names)


def process_quote_data():
    """
    Write fetched quote data as a CSV.
    """
    quote_data = api.get_quote_data(",".join(SYMBOLS))

    field_names = list(quote_data[0].keys())
    lib.write_csv(CSV_OUT_QUOTE_DATA, quote_data, field_names)


def main():
    """
    Command-line entry-point.
    """
    process_chart_data()
    process_quote_data()


if __name__ == "__main__":
    main()
