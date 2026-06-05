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
from typing import Optional

import pandas as pd

# Configure a module-level logger
logger = logging.getLogger(__name__)
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


def load_data(
    scorecard_path: str = "../data/processed/fund_scorecard.csv",
    master_path: str = "../data/raw/01_fund_master.csv",
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


def save_recommendations(df: pd.DataFrame, risk: str, output_path: str, top_n: int = 3) -> str:
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
    recommendations = recommend(df, risk, top_n=top_n)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    recommendations.to_csv(output_path, index=False)
    abs_path = os.path.abspath(output_path)
    logger.info("Saved recommendations to %s", abs_path)
    return abs_path


if __name__ == "__main__":
    # Basic CLI behavior when executed directly
    df = load_data()
    out = save_recommendations(df, "High", os.path.join("scripts", "recommendations_high.csv"))
    logger.info("Completed main run; output=%s", out)
