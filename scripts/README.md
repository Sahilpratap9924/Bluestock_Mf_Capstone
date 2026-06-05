Scripts folder

Contains small utility scripts used by the analysis and report generation.

How to use

- `recommender.py`: exposes `load_data()`, `recommend()`, and `save_recommendations()` functions. Import from `scripts.recommender` or run directly.
- `generate_report_template_fixed.py` (if present): generates a PDF template in `reports/`.

Run the master pipeline from project root:

```bash
python run_pipeline.py
```
