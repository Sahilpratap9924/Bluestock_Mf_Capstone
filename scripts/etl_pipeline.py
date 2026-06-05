"""ETL pipeline runner utilities.

Provides a simple programmatic way to execute notebook-based ETL steps or script-based ETL.

Functions
- `run_etl()` - run notebooks in the canonical order using papermill or nbconvert.

This is a lightweight helper — adapt to your preferred orchestration (Airflow, Prefect, Makefile).
"""

from __future__ import annotations

import logging
import os
import subprocess
import sys
from typing import List, Optional

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NOTEBOOK_DIR = os.path.join(ROOT, 'notebooks')

DEFAULT_NOTEBOOK_ORDER = [
    '01_data_ingestion.ipynb',
    '02_data_cleaning.ipynb',
    '03_eda_analysis.ipynb',
    '04_performance_analytics.ipynb',
    '05_Advanced_Analytics.ipynb',
]


def run_notebook(path: str) -> None:
    """Execute a single notebook using `jupyter nbconvert --execute`.

    Uses the current Python environment's `jupyter` module. Output notebook is discarded by default.
    """
    logger.info('Executing notebook: %s', path)
    try:
        subprocess.run([
            sys.executable, '-m', 'nbconvert', '--to', 'notebook', '--execute', path, '--ExecutePreprocessor.timeout=600'
        ], check=True)
        logger.info('Finished: %s', path)
    except subprocess.CalledProcessError as exc:
        logger.exception('Notebook execution failed: %s', exc)
        raise


def run_etl(notebooks: Optional[List[str]] = None) -> None:
    """Run ETL notebooks in order.

    If `notebooks` is None, runs `DEFAULT_NOTEBOOK_ORDER` from the `notebooks/` folder.
    """
    if notebooks is None:
        notebooks = [os.path.join(NOTEBOOK_DIR, n) for n in DEFAULT_NOTEBOOK_ORDER]
    for nb in notebooks:
        run_notebook(nb)


if __name__ == '__main__':
    run_etl()
