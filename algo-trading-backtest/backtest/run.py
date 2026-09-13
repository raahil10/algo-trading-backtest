"""
Runs the full pipeline for one ticker: fetch data, apply the MA crossover
signal, compute returns and transaction costs, then summarize performance.
"""

from __future__ import annotations

from .data import get_price_data
from .strategy import add_ma, signal
from .portfolio import compute_returns, apply_transaction_costs
from .metrics import (
    total_return,
    annualized_return,
    annualized_volatility,
    sharpe_ratio,
    max_drawdown,
    win_rate,
)


def run_backtest(ticker: str, start: str, end: str, fast: int = 50, slow: int = 200) -> dict:
    """
    Run the MA crossover backtest for a single ticker and return a summary
    dict of performance metrics (net of transaction costs).
    """
    df = get_price_data(ticker, start, end)
    df = add_ma(df, fast=fast, slow=slow)
    df = signal(df)
    df = compute_returns(df)
    df = apply_transaction_costs(df)

    cum_strategy = df["cum_net_strategy_returns"]
    pct_strategy = df["net_strategy_returns"]
    ann_return = annualized_return(cum_strategy)
    ann_vol = annualized_volatility(pct_strategy)

    return {
        "ticker": ticker,
        "total_return": total_return(cum_strategy),
        "annualized_return": ann_return,
        "annualized_volatility": ann_vol,
        "sharpe_ratio": sharpe_ratio(ann_return, ann_vol),
        "max_drawdown": max_drawdown(cum_strategy) * 100,
        "win_rate": win_rate(pct_strategy),
    }
