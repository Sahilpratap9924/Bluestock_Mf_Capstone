"""Fetch latest NAV data from a remote source with CLI.

This module provides `fetch_live_navs` and `save_live_navs` helpers and a small CLI
so you can run:

    python scripts/live_nav_fetch.py --url https://.../navs.csv --out data/raw/latest_navs.csv

If `--url` is not provided the script will fall back to the `LIVE_NAV_URL` environment variable.
"""

from __future__ import annotations

import argparse
import io
import logging
import os
import sys
from typing import Optional

import pandas as pd

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


def fetch_live_navs(url: str, timeout: int = 30) -> pd.DataFrame:
    """Fetch NAVs from `url` and return a DataFrame.

    Expects a CSV payload that `pandas.read_csv` can parse.
    """
    try:
        import requests
    except Exception as exc:
        logger.error('requests is required to fetch remote NAVs: %s', exc)
        raise

    logger.info('Requesting NAVs from %s', url)
    resp = requests.get(url, timeout=timeout)
    resp.raise_for_status()

    text = resp.text
    df = pd.read_csv(io.StringIO(text))
    logger.info('Downloaded %d rows', len(df))
    return df


def save_live_navs(df: pd.DataFrame, out_path: str) -> None:
    """Save DataFrame to CSV, creating parent directories as needed."""
    out_dir = os.path.dirname(out_path) or '.'
    os.makedirs(out_dir, exist_ok=True)
    df.to_csv(out_path, index=False)
    logger.info('Saved live NAVs to %s', out_path)


def _default_output_path() -> str:
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(project_root, 'data', 'raw', 'latest_navs.csv')


def parse_args(argv: Optional[list[str]] = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description='Fetch live NAV CSV and save locally')
    p.add_argument('--url', '-u', help='CSV endpoint URL for NAVs (falls back to LIVE_NAV_URL env var)')
    p.add_argument('--out', '-o', help='Output CSV path', default=None)
    p.add_argument('--timeout', type=int, default=30, help='HTTP timeout in seconds')
    return p.parse_args(argv)


def main(argv: Optional[list[str]] = None) -> int:
    args = parse_args(argv)
    url = args.url or os.environ.get('LIVE_NAV_URL')
    if not url:
        logger.error('No URL provided. Set --url or the LIVE_NAV_URL environment variable.')
        return 2

    out_path = args.out or _default_output_path()

    try:
        df = fetch_live_navs(url, timeout=args.timeout)
        save_live_navs(df, out_path)
    except Exception:
        logger.exception('Failed to fetch or save live NAVs')
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
