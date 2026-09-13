# Algorithmic Trading Backtest: Moving Average Crossover

A backtest of a moving average (MA) crossover strategy on AAPL, MSFT, and
SPY, benchmarked against simple buy-and-hold, with transaction costs and
standard performance metrics.

## What this actually does

A **moving average crossover** is one of the oldest trend-following
strategies: track a short-term average price (e.g. 50 days) and a
long-term average (e.g. 200 days). When the short-term average rises
above the long-term one, the trend is considered "up" and the strategy
goes long. When it falls back below, the strategy exits.

This project:
1. Downloads historical daily prices for a ticker
2. Computes the 50-day and 200-day moving averages
3. Generates a long/flat signal from the crossover
4. Converts that signal into actual daily returns (using *yesterday's*
   signal, since you can't trade on a signal you don't have yet)
5. Subtracts a transaction cost every time the signal actually changes
   (i.e. every time a real trade would happen)
6. Compares the result against simply buying and holding the stock

## The metrics

| Metric | What it tells you |
|---|---|
| **Total return** | Overall % gain/loss across the whole backtest period |
| **Annualized return** | Total return converted into a "per year" rate, so periods of different lengths can be compared fairly |
| **Annualized volatility** | How much the strategy's daily returns bounce around, scaled to a yearly figure |
| **Sharpe ratio** | Return earned *per unit of risk taken* — higher is better; it's what separates "made money" from "made money without taking on huge swings" |
| **Max drawdown** | The worst peak-to-trough loss during the backtest — a measure of the worst pain you'd have sat through |
| **Win rate** | Of the days the strategy was actually active in a trade, what % were profitable |

## Project structure

```
algo-trading-backtest/
├── backtest/
│   ├── __init__.py
│   ├── data.py        # fetches price data via yfinance
│   ├── strategy.py     # MA crossover signal logic
│   ├── portfolio.py    # turns signals into returns + transaction costs
│   ├── metrics.py       # performance metrics
│   └── run.py           # ties everything together into run_backtest()
├── examples/
│   └── run_summary.py   # runs the backtest across AAPL/MSFT/SPY, prints a summary table
├── tests/
│   └── test_metrics.py  # metric correctness checks on synthetic data (no internet needed)
├── requirements.txt
└── README.md
```

## Setup

```bash
git clone https://github.com/<your-username>/algo-trading-backtest.git
cd algo-trading-backtest
pip install -r requirements.txt
```

## Usage

**Run the full backtest across all three tickers:**
```bash
python examples/run_summary.py
```

**As a library, in your own code:**
```python
from backtest import run_backtest

result = run_backtest("AAPL", start="2019-01-01", end="2024-01-01")
print(result)
```

**Run tests** (checks the metric formulas against known synthetic values —
doesn't require an internet connection):
```bash
python -m pytest tests/
```
## Sample output

Running `examples/run_summary.py` on 2019–2024 daily data:

| ticker | total_return | annualized_return | annualized_volatility | sharpe_ratio | max_drawdown | win_rate |
|---|---|---|---|---|---|---|
| AAPL | 186.76% | 31.12% | 27.42% | 0.97 | -31.43% | 53.39% |
| MSFT | 197.75% | 31.86% | 24.79% | 1.10 | -28.04% | 55.03% |
| SPY | 45.40% | 19.70% | 16.15% | 0.93 | -33.72% | 56.04% |

Note the drawdowns: even the best-performing tickers here saw the strategy
lose roughly 28–34% of its value at some point before recovering.

## Assumptions and limitations

This is a simplified backtest: it assumes trades execute exactly at the
close price with no slippage, uses a flat per-trade cost rather than a
realistic bid-ask spread, and doesn't account for dividends beyond what
`auto_adjust=True` bakes in. It also tests only one parameter set (50/200
day) rather than optimizing or validating out-of-sample, so results here
shouldn't be read as "this strategy works" — a natural next step would be
walk-forward testing across multiple parameter sets and time periods to
check the edge isn't just a lucky fit.

## License

MIT — see [LICENSE](LICENSE).
