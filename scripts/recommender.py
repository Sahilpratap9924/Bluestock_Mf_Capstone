"""Small recommender utilities used by the project.

This module provides helpers to load the fund scorecard and master
metadata, compute top-N recommendations for a given risk category,
and persist those recommendations to CSV.

Functions:
  - load_data(scorecard_path, master_path): return merged DataFrame
  - recommend(df, risk, top_n): return top-N recommendations DataFrame
  - save_recommendations(df, risk, output_path, top_n): write CSV

This module is intended to be imported by automated pipelines; avoid
printing from library functions. Use logging for status messages.
"""

from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import Optional, Union

import pandas as pd

# Configure a module-level logger
logger = logging.getLogger(__name__)
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SCORECARD_PATH = ROOT / "data" / "processed" / "fund_scorecard.csv"
DEFAULT_MASTER_PATH = ROOT / "data" / "raw" / "01_fund_master.csv"


def load_data(
    scorecard_path: Optional[Union[str, Path]] = None,
    master_path: Optional[Union[str, Path]] = None,
) -> pd.DataFrame:
    """Load and merge the fund scorecard and master metadata.

    Parameters
    ----------
    scorecard_path : str
        Path to the processed `fund_scorecard.csv` file.
    master_path : str
        Path to the raw `01_fund_master.csv` file.

    Returns
    -------
    pandas.DataFrame
        Merged DataFrame on column ``amfi_code``.
    """
    if scorecard_path is None:
        scorecard_path = DEFAULT_SCORECARD_PATH
    if master_path is None:
        master_path = DEFAULT_MASTER_PATH

    scorecard = pd.read_csv(scorecard_path)
    master = pd.read_csv(master_path)
    merged = scorecard.merge(master, on="amfi_code")
    logger.debug("Loaded scorecard (%s rows) and master (%s rows)", len(scorecard), len(master))
    return merged


def recommend(df: pd.DataFrame, risk: str, top_n: int = 3) -> pd.DataFrame:
    """Return the top-N recommended schemes for a given risk category.

    The ranking metric is ``sharpe_ratio`` in descending order.
    """
    result = (
        df[df["risk_category"] == risk]
        .sort_values("sharpe_ratio", ascending=False)
        .head(top_n)
    )
    return result[["scheme_name", "risk_category", "sharpe_ratio"]]


def save_recommendations(df: pd.DataFrame, risk: str, output_path: Union[str, Path], top_n: int = 3) -> str:
    """Compute recommendations and save to CSV.

    Parameters
    ----------
    df : pandas.DataFrame
        The merged scorecard/master DataFrame.
    risk : str
        Risk category to filter on (e.g., 'High').
    output_path : str
        Path where recommendations CSV will be written.
    top_n : int
        Number of top recommendations to save.

    Returns
    -------
    str
        The absolute path to the written file.
    """
    output_path = Path(output_path)
    recommendations = recommend(df, risk, top_n=top_n)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    recommendations.to_csv(output_path, index=False)
    abs_path = str(output_path.resolve())
    logger.info("Saved recommendations to %s", abs_path)
    return abs_path


if __name__ == "__main__":
    # Basic CLI behavior when executed directly
    df = load_data()
    out = save_recommendations(df, "High", ROOT / "scripts" / "recommendations_high.csv")
    logger.info("Completed main run; output=%s", out)
