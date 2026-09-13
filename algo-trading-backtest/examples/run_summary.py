"""
Runs the backtest across multiple tickers and prints a summary table,
same as the original script.

Run with:
    python examples/run_summary.py
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pandas as pd

from backtest import run_backtest

TICKERS = ["AAPL", "MSFT", "SPY"]
START = "2019-01-01"
END = "2024-01-01"

if __name__ == "__main__":
    results = [run_backtest(ticker, START, END) for ticker in TICKERS]
    summary = pd.DataFrame(results).set_index("ticker")
    print(summary)
