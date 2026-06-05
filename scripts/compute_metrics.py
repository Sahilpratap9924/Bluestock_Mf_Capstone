"""Compute performance metrics from NAV / returns data.

Provides helper functions to compute periodic returns, rolling Sharpe, drawdown, and other common metrics.
"""

from __future__ import annotations

import logging
from typing import Optional

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')


def compute_returns(df: pd.DataFrame, price_col: str = 'nav', date_col: str = 'date') -> pd.Series:
    """Compute simple period returns from a price/nav column.

    Expects `df` indexed by time or containing a `date_col` which will not be modified.
    Returns a pandas Series of returns aligned with the input DataFrame (first return will be NaN).
    """
    prices = df[price_col].astype(float)
    returns = prices.pct_change()
    return returns


def rolling_sharpe(returns: pd.Series, window: int = 90, trading_days: int = 252) -> pd.Series:
    """Compute rolling Sharpe ratio (annualized) using a lookback `window`.

    Sharpe = mean / std * sqrt(trading_days)
    """
    mean = returns.rolling(window).mean()
    std = returns.rolling(window).std()
    sharpe = (mean / std) * np.sqrt(trading_days)
    return sharpe


def max_drawdown(wealth_index: pd.Series) -> float:
    """Return maximum drawdown from a wealth index (cumulative returns series)."""
    peak = wealth_index.cummax()
    drawdown = (wealth_index - peak) / peak
    return drawdown.min()


def compute_all_metrics(df: pd.DataFrame, price_col: str = 'nav', date_col: str = 'date', window: int = 90) -> pd.DataFrame:
    """Compute a small set of metrics and return a DataFrame with added columns.

    Adds columns: `returns`, `rolling_sharpe_{window}`
    """
    df = df.copy()
    df['returns'] = compute_returns(df, price_col=price_col, date_col=date_col)
    df[f'rolling_sharpe_{window}'] = rolling_sharpe(df['returns'], window=window)
    return df


if __name__ == '__main__':
    # Example usage: read a processed NAV file and write metrics
    import os
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    in_path = os.path.join(root, 'data', 'processed', 'clean_nav.csv')
    out_path = os.path.join(root, 'data', 'processed', 'nav_with_metrics.csv')

    if not os.path.exists(in_path):
        logger.error('Input file not found: %s', in_path)
    else:
        df = pd.read_csv(in_path, parse_dates=['date'])
        out = compute_all_metrics(df)
        out.to_csv(out_path, index=False)
        logger.info('Wrote metrics to %s', out_path)
