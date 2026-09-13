"""
Turns a trading signal into actual returns: the buy-and-hold return, the
signal-driven strategy return, cumulative performance of both, and the
cost of actually trading the signal.
"""

from __future__ import annotations

import pandas as pd


def compute_returns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add daily stock returns and strategy returns.

    Signal is shifted by 1 day so today's return uses yesterday's signal —
    otherwise the backtest would be trading on information (today's close)
    that wasn't actually known yet at the start of the day.
    """
    df["stock_return"] = df["Close"].pct_change()
    df["strategy_return"] = df["Signal"].shift(1) * df["stock_return"]
    return df


def cumulative_comparison(df: pd.DataFrame) -> pd.DataFrame:
    """Add cumulative growth-of-$1 columns for both the strategy and buy-and-hold."""
    df["strategy"] = (1 + df["strategy_return"]).cumprod()
    df["hold"] = (1 + df["stock_return"]).cumprod()
    return df


def apply_transaction_costs(df: pd.DataFrame, cost: float = 0.001) -> pd.DataFrame:
    """
    Subtract a per-trade cost each time the signal changes (i.e. each time
    a trade actually happens), then recompute cumulative net returns.
    """
    trade_day = df["Signal"].diff().abs().fillna(0)
    df["net_strategy_returns"] = df["strategy_return"] - (trade_day * cost)
    df["cum_net_strategy_returns"] = (1 + df["net_strategy_returns"].fillna(0)).cumprod()
    return df
