"""Interpolate two-asset pool weights over time and evaluate spot prices and scenario quotes."""

from .common import (
    number,
    integer,
    identity,
    records,
    chronology,
    allocate,
    result,
    validate_document,
)
from decimal import Decimal


def _analyze(d):
    start = integer(d["start"])
    end = integer(d["end"])
    w0 = number(d["start_weight"], maximum=1)
    w1 = number(d["end_weight"], maximum=1)
    x = number(d["balance_in"], minimum="0.000000000000000001")
    y = number(d["balance_out"], minimum="0.000000000000000001")
    if end <= start or w0 in (0, 1) or w1 in (0, 1):
        raise ValueError("invalid weight schedule")
    rows = []
    for s in records(d["scenarios"], "id"):
        t = integer(s["timestamp"])
        progress = number(min(max(t - start, 0), end - start)) / (end - start)
        w = w0 + (w1 - w0) * progress
        spot = (y / (1 - w)) / (x / w)
        amount = number(s["amount_in"])
        output = float(y) * (1 - (float(x / (x + amount))) ** float(w / (1 - w)))
        rows.append(
            {
                "id": s["id"],
                "weight_in": w,
                "spot_price": spot,
                "output": output,
                "timestamp": t,
            }
        )
    return result({"scenarios": rows})


def analyze(document):
    validate_document(document)
    try:
        return result(_analyze(document))
    except (KeyError, TypeError, ArithmeticError, RecursionError) as error:
        raise ValueError("invalid domain input: " + str(error)) from error
