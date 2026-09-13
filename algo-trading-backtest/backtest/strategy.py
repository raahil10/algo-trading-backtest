"""
Moving average crossover strategy: generates a long/flat signal based on
a fast moving average crossing above or below a slow moving average.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def add_ma(df: pd.DataFrame, fast: int = 50, slow: int = 200) -> pd.DataFrame:
    """Add fast and slow moving average columns to the DataFrame."""
    df["fast_ma"] = df["Close"].rolling(window=fast).mean()
    df["slow_ma"] = df["Close"].rolling(window=slow).mean()
    return df


def signal(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add a Signal column: 1 when the fast MA is above the slow MA (long),
    0 otherwise (flat). Requires add_ma() to have been run first.
    """
    df["Signal"] = np.where(df["fast_ma"] > df["slow_ma"], 1, 0)
    return df
