Scripts folder

Contains small utility scripts used by the analysis and report generation.

How to use

- `recommender.py`: exposes `load_data()`, `recommend()`, and `save_recommendations()` functions. Import from `scripts.recommender` or run directly.
- `generate_report_template_fixed.py` (if present): generates a PDF template in `reports/`.

Run the master pipeline from project root:

```bash
python run_pipeline.py
```

Scheduled ETL

- `scripts/auto_etl.py`: fetches NAV data and then runs the pipeline.
- `scripts/setup_etl_schedule.ps1`: registers a Windows scheduled task that runs the ETL every weekday at 8 PM.

Example:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/setup_etl_schedule.ps1 -MfapiUrl 'https://api.mfapi.in/mf/<scheme-code>'
```
