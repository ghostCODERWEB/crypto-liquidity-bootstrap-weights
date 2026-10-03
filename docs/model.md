# Liquidity bootstrapping weight schedule: domain model

Interpolate two-asset pool weights over time and evaluate spot prices and scenario quotes.

## Input contract

| Field | Example JSON shape |
|---|---|
| `start` | `int` |
| `end` | `int` |
| `start_weight` | `str` |
| `end_weight` | `str` |
| `balance_in` | `int` |
| `balance_out` | `int` |
| `scenarios` | `list` |

The fixture includes nested records and concrete units. Engine validation is authoritative: required keys are read explicitly, identifiers must be nonempty, integer amounts reject booleans, record IDs are unique where indicated, and chronological logs reject reversed timestamps. A document is bounded to 100,000 values, depth 25 and 10,000 entries per collection. Domain-specific tighter bounds apply where required. Extra fields are tolerated and ignored.

## Calculation and outputs

The domain function executes on supplied data without mutation. Results include intermediate allocations, traces or per-scenario records so aggregate outputs can be reconciled. Four known-answer assertions in `tests/test_domain.py` cover the example independently of the generated regression output. Inspect `cryptolab/engine.py` for the executable algorithm and explicit rejection paths.

## Explicit assumptions

Weights interpolate linearly and quotes use floating-point powers. Reserves stay fixed across independent scenarios; this is not a deployed LBP implementation.

Input correctness and completeness remain the caller's responsibility. Offline results are educational and cannot prove external account ownership, protocol safety, source authenticity or future outcomes. Decimal precision follows Python's default 28 significant digits. Do not use illustrative fixture numbers as market data.
