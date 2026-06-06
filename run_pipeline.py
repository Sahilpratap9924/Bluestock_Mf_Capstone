"""Master pipeline runner for Bluestock MF Capstone.

Usage:
    python run_pipeline.py

This script will:
- Run the recommender to generate top recommendations CSV
- If a report generator script exists in `scripts/`, run it to produce the PDF

It is intentionally simple and idempotent.
"""

import logging
import subprocess
import sys
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger('run_pipeline')

ROOT = Path(__file__).resolve().parent
SCRIPTS_DIR = ROOT / 'scripts'


def run_recommender():
    """Run recommender.save_recommendations using the local scripts/recommender.py module."""
    sys.path.insert(0, str(SCRIPTS_DIR))
    try:
        import recommender
    except Exception as exc:
        logger.error('Could not import recommender: %s', exc)
        return

    try:
        df = recommender.load_data()
    except Exception as exc:
        logger.error('Failed to load data for recommender: %s', exc)
        return

    out_path = SCRIPTS_DIR / 'recommendations_high.csv'
    try:
        recommender.save_recommendations(df, 'High', out_path)
        logger.info('Recommendations written to %s', out_path.resolve())
    except Exception as exc:
        logger.exception('Failed to save recommendations: %s', exc)


def run_report_generator():
    """If a report generator script exists, execute it as a subprocess."""
    candidates = [
        SCRIPTS_DIR / 'generate_report_template_fixed.py',
        SCRIPTS_DIR / 'generate_report_template.py',
    ]
    for c in candidates:
        if c.exists():
            logger.info('Running report generator: %s', c)
            try:
                subprocess.run([sys.executable, str(c)], check=True)
                logger.info('Report generation completed.')
            except subprocess.CalledProcessError as e:
                logger.error('Report generator failed: %s', e)
            return
    logger.info('No report generator found in scripts/. Skipping report step.')


def main():
    logger.info('Starting pipeline')
    run_recommender()
    run_report_generator()
    logger.info('Pipeline finished')


if __name__ == '__main__':
    main()
