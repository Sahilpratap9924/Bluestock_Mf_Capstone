"""Fetch NAV data from mfapi.in and run the ETL pipeline.

This script is intended to be run on a schedule. It fetches the latest NAV CSV from
mfapi.in (or any other compatible CSV endpoint) and then executes the project pipeline.
"""

from __future__ import annotations

import argparse
import logging
import os
import subprocess
import sys
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = ROOT / 'scripts'
DEFAULT_OUTPUT_PATH = ROOT / 'data' / 'raw' / 'latest_navs.csv'


def parse_args(argv: Optional[list[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Run the scheduled ETL pipeline with live NAV fetch.')
    parser.add_argument('--url', '-u', help='CSV endpoint URL to fetch NAVs from')
    parser.add_argument('--scheme-code', help='mfapi.in scheme code to fetch from https://api.mfapi.in/mf/<scheme-code>')
    parser.add_argument('--out', '-o', help='Output CSV path', default=str(DEFAULT_OUTPUT_PATH))
    parser.add_argument('--timeout', type=int, default=30, help='HTTP timeout in seconds')
    parser.add_argument('--skip-pipeline', action='store_true', help='Fetch NAVs only and skip pipeline execution')
    return parser.parse_args(argv)


def resolve_nav_url(url: Optional[str], scheme_code: Optional[str]) -> str:
    if url:
        return url
    if scheme_code:
        return f'https://api.mfapi.in/mf/{scheme_code}'
    raise ValueError('Either --url or --scheme-code must be provided.')


def run_live_nav_fetch(url: str, out_path: str, timeout: int) -> None:
    sys.path.insert(0, str(SCRIPTS_DIR))
    try:
        import live_nav_fetch
    except Exception as exc:
        logger.exception('Failed to import live_nav_fetch: %s', exc)
        raise

    return_code = live_nav_fetch.main(['--url', url, '--out', out_path, '--timeout', str(timeout)])
    if return_code != 0:
        raise RuntimeError(f'live_nav_fetch failed with exit code {return_code}')


def run_pipeline() -> None:
    pipeline_script = ROOT / 'run_pipeline.py'
    logger.info('Executing pipeline: %s', pipeline_script)
    subprocess.run([sys.executable, str(pipeline_script)], check=True)


def main(argv: Optional[list[str]] = None) -> int:
    args = parse_args(argv)
    url = resolve_nav_url(args.url, args.scheme_code)
    out_path = args.out

    logger.info('Starting scheduled ETL: fetch NAV from %s', url)
    try:
        run_live_nav_fetch(url, out_path, args.timeout)
    except Exception as exc:
        logger.exception('NAV fetch failed: %s', exc)
        return 1

    if args.skip_pipeline:
        logger.info('Skipping pipeline execution as requested.')
        return 0

    try:
        run_pipeline()
    except subprocess.CalledProcessError as exc:
        logger.exception('Pipeline execution failed: %s', exc)
        return 2

    logger.info('Scheduled ETL completed successfully.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
