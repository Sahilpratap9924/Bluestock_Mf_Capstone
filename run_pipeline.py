"""Master pipeline runner for Bluestock MF Capstone.

Usage:
    python run_pipeline.py

This script will:
- Run the recommender to generate top recommendations CSV
- If a report generator script exists in `scripts/`, run it to produce the PDF

It is intentionally simple and idempotent.
"""

import logging
import os
import subprocess
import sys

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger('run_pipeline')

ROOT = os.path.dirname(os.path.abspath(__file__))
SCRIPTS_DIR = os.path.join(ROOT, 'scripts')


def run_recommender():
    """Run recommender.save_recommendations using the local scripts/recommender.py module."""
    sys.path.insert(0, SCRIPTS_DIR)
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

    out_path = os.path.join('scripts', 'recommendations_high.csv')
    try:
        recommender.save_recommendations(df, 'High', out_path)
        logger.info('Recommendations written to %s', os.path.abspath(out_path))
    except Exception as exc:
        logger.exception('Failed to save recommendations: %s', exc)


def run_report_generator():
    """If a report generator script exists, execute it as a subprocess."""
    candidates = [
        os.path.join(SCRIPTS_DIR, 'generate_report_template_fixed.py'),
        os.path.join(SCRIPTS_DIR, 'generate_report_template.py'),
    ]
    for c in candidates:
        if os.path.exists(c):
            logger.info('Running report generator: %s', c)
            try:
                subprocess.run([sys.executable, c], check=True)
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
