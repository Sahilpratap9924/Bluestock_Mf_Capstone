"""Fetch latest NAV data from a remote source.

This module provides a minimal `fetch_live_navs` function that attempts to download CSV-formatted NAV data
from a given URL and return a `pandas.DataFrame`.

"""

from __future__ import annotations

import logging
import os
from typing import Optional

import pandas as pd

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


def fetch_live_navs(url: str, timeout: int = 30) -> pd.DataFrame:
    """Fetch NAVs from `url` and return a DataFrame.

    The function expects a CSV response that can be parsed by `pandas.read_csv`.
    """
    try:
        import requests
    except Exception as exc:
        logger.error('requests is required to fetch remote NAVs: %s', exc)
        raise

    logger.info('Requesting NAVs from %s', url)
    resp = requests.get(url, timeout=timeout)
    resp.raise_for_status()

    # Let pandas parse the CSV content
    df = pd.read_csv(pd.compat.StringIO(resp.text)) if hasattr(pd, 'compat') else pd.read_csv(pd.io.common.StringIO(resp.text))
    logger.info('Downloaded %d rows', len(df))
    return df


def save_live_navs(df: pd.DataFrame, out_path: str) -> None:
    os.makedirs(os.path.dirname(out_path) or '.', exist_ok=True)
    df.to_csv(out_path, index=False)
    logger.info('Saved live NAVs to %s', out_path)


if __name__ == '__main__':
    # Example: write to data/raw/latest_navs.csv if environment provides URL
    sample_url = os.environ.get('LIVE_NAV_URL')
    if not sample_url:
        logger.error('Set LIVE_NAV_URL environment variable to a CSV endpoint to fetch live NAVs')
    else:
        df = fetch_live_navs(sample_url)
        out = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'raw', 'latest_navs.csv')
        save_live_navs(df, out)
