"""
Price data fetching via yfinance.
"""

from __future__ import annotations

import pandas as pd
import yfinance as yf


def get_price_data(ticker: str, start: str, end: str) -> pd.DataFrame:
    """
    Download daily OHLCV data for a ticker and return a clean DataFrame
    with a flat 'Close' column (yfinance can return multi-level columns).
    """
    df = yf.download(ticker, start=start, end=end, group_by="column", auto_adjust=True)
    df.columns = df.columns.get_level_values(0)
    return df
