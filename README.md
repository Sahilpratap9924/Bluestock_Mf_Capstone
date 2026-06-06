Bluestock MF Capstone

## Project overview

Bluestock MF Capstone is a reproducible analysis and reporting project for mutual fund analytics. It contains raw data, ETL and cleaning notebooks, analysis notebooks, scripts for utilities and report generation, and a dashboard export folder for visualization.

## Quick start

1. Create and activate a virtual environment (recommended):
   - On Windows (PowerShell):

     ```powershell
     python -m venv .venv
     .\.venv\Scripts\Activate.ps1
     pip install --upgrade pip
     pip install -r requirements.txt
     ```

   - On macOS / Linux (bash):

     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     pip install --upgrade pip
     pip install -r requirements.txt
     ```

2. Run the pipeline (recommender + report generator):

   ```bash
   python run_pipeline.py
   ```

## Repository layout

- data/: Raw and processed datasets
  - data/raw/: original source CSVs
  - data/processed/: cleaned and derived datasets used for analysis
- notebooks/: Jupyter notebooks for ETL, cleaning, EDA and analysis
  - Recommended order: `01_data_ingestion.ipynb` -> `02_data_cleaning.ipynb` -> `03_eda_analysis.ipynb` -> `04_performance_analytics.ipynb` -> `05_Advanced_Analytics.ipynb`
- scripts/: Reusable Python scripts for recommendations, report generation, and helpers
- reports/: Generated charts and final PDFs (e.g., `Final_Report_Template.pdf`)
- dashboard/: Dashboard source or exported static files / app
- sql/: Helpful queries and schema definitions

## How to run ETL and regenerate processed data

- Option A — Notebooks (interactive):
  - Open Jupyter Lab/Notebook and run notebooks in the recommended order to reproduce ETL and analysis.

- Option B — Programmatic pipeline runner:
  - The repository includes a simple runner: `run_pipeline.py`. It executes the recommender and will call any report-generator script present in `scripts/`:

    ```bash
    python run_pipeline.py
    ```

- To deploy the ETL pipeline as a scheduled task on Windows, use `scripts/setup_etl_schedule.ps1` with an mfapi.in URL.

- Option C — Execute notebooks non-interactively:
  - Install `papermill` or use `jupyter nbconvert --execute` to run notebooks end-to-end. Example with `nbconvert`:

    ```bash
    jupyter nbconvert --to notebook --execute notebooks/01_data_ingestion.ipynb --output out/01_data_ingestion_executed.ipynb
    ```

## Outputs

- Processed datasets are written to `data/processed/`.
- Charts and the generated report PDF are written to `reports/`.
- Recommendations (CSV) are written to `scripts/` when produced by the recommender.

## Opening the dashboard

- See `dashboard/README.md` for specifics about the dashboard export or app.
- If the dashboard is a static export, open the relevant HTML files in `dashboard/` with a browser.
- If the dashboard is a Streamlit app (check for `dashboard/app.py`), run:

  ```bash
  streamlit run dashboard/app.py
  ```

## Contributing & development notes

- Use the `scripts/README.md` for developer-focused instructions.
- Please follow the existing logging pattern in `scripts/` (module-level logger) when adding or editing scripts.

## License & contact

This repository is a capstone project. For questions or to report issues, open an issue or contact the project owner.
