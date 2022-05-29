def print_debug(value) -> None:
    """
    Print object as friendly JSON value.
    """
    print(json.dumps(value, indent=4))


import csv
import json
import sys
from typing import List


def print_error(value):
    """
    Print message to stderr.
    """
    print(value, file=sys.stderr)


def write_csv(path: str, out_data: List[dict], field_names: List[str]) -> None:
    """
    Write given data to a CSV file.
    """
    with open(path, "w", encoding="utf-8") as f_out:
        writer = csv.DictWriter(f_out, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(out_data)
