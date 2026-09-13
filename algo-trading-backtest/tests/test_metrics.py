"""
Sanity checks for the performance metrics, using synthetic data so no
internet connection or live market data is needed to run these.

Run with:
    python -m pytest tests/
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import numpy as np
import pandas as pd

from backtest.metrics import (
    total_return,
    annualized_return,
    annualized_volatility,
    sharpe_ratio,
    max_drawdown,
    win_rate,
)

# A cumulative return series representing $1 growing steadily to $1.20,
# with a dip in the middle (for testing drawdown).
cum_series = pd.Series([1.0, 1.05, 1.10, 0.95, 1.00, 1.20])
daily_returns = pd.Series([0.0, 0.02, -0.01, 0.03, 0.0, -0.015, 0.01])


def test_total_return():
    result = total_return(cum_series)
    assert np.isclose(result, 20.0)


def test_annualized_return_positive_for_growth():
    result = annualized_return(cum_series, periods_per_year=252)
    assert result > 0


def test_annualized_volatility_non_negative():
    result = annualized_volatility(daily_returns)
    assert result >= 0


def test_sharpe_ratio_matches_formula():
    result = sharpe_ratio(ann_return=0.15, ann_vol=0.20, risk_free_rate=0.0465)
    expected = (0.15 - 0.0465) / 0.20
    assert np.isclose(result, expected)


def test_max_drawdown_is_negative_when_there_is_a_dip():
    result = max_drawdown(cum_series)
    # Peak of 1.10 to trough of 0.95 is roughly a -13.6% drawdown
    assert result < 0
    assert np.isclose(result, (0.95 / 1.10) - 1, atol=1e-8)


def test_max_drawdown_zero_for_monotonic_growth():
    always_up = pd.Series([1.0, 1.1, 1.2, 1.3])
    assert max_drawdown(always_up) == 0


def test_win_rate_ignores_zero_return_days():
    returns = pd.Series([0.0, 0.01, -0.02, 0.03, 0.0])
    # 2 of 3 active (non-zero) days are positive
    assert np.isclose(win_rate(returns), (2 / 3) * 100)


def test_win_rate_zero_when_no_active_days():
    returns = pd.Series([0.0, 0.0, 0.0])
    assert win_rate(returns) == 0


if __name__ == "__main__":
    test_total_return()
    test_annualized_return_positive_for_growth()
    test_annualized_volatility_non_negative()
    test_sharpe_ratio_matches_formula()
    test_max_drawdown_is_negative_when_there_is_a_dip()
    test_max_drawdown_zero_for_monotonic_growth()
    test_win_rate_ignores_zero_return_days()
    test_win_rate_zero_when_no_active_days()
    print("All tests passed.")
