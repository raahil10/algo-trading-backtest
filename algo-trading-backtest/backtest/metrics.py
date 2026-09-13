"""
Standard performance metrics for evaluating a backtested strategy.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def total_return(cum_series: pd.Series) -> float:
    """Total percentage return over the whole backtest period."""
    final_return = cum_series.iloc[-1]
    return (final_return - 1) * 100


def annualized_return(cum_series: pd.Series, periods_per_year: int = 252) -> float:
    """Compound annual growth rate implied by the cumulative return series."""
    final_return = cum_series.iloc[-1]
    years = len(cum_series) / periods_per_year
    return (1 + final_return) ** (1 / years) - 1


def annualized_volatility(returns: pd.Series, periods_per_year: int = 252) -> float:
    """Annualized standard deviation of daily returns."""
    daily_vol = returns.std()
    return daily_vol * np.sqrt(periods_per_year)


def sharpe_ratio(ann_return: float, ann_vol: float, risk_free_rate: float = 0.0465) -> float:
    """Risk-adjusted return: excess return per unit of volatility."""
    return (ann_return - risk_free_rate) / ann_vol


def max_drawdown(cum_series: pd.Series) -> float:
    """Largest peak-to-trough decline in the cumulative return series."""
    running_max = cum_series.cummax()
    drawdown = (cum_series / running_max) - 1
    return drawdown.min()


def win_rate(returns: pd.Series) -> float:
    """Percentage of active trading days (non-zero return) that were positive."""
    active = returns[returns != 0]
    if len(active) == 0:
        return 0
    winning_days = np.sum(active > 0)
    return (winning_days / len(active)) * 100
