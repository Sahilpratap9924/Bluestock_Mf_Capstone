CREATE TABLE dim_fund(

amfi_code TEXT PRIMARY KEY,

scheme_name TEXT,

fund_house TEXT,

category TEXT,

sub_category TEXT,

expense_ratio_pct REAL,

risk_category TEXT

);

CREATE TABLE fact_nav(

amfi_code TEXT,

date DATE,

nav REAL,

daily_return REAL

);

CREATE TABLE fact_transactions(

investor_id TEXT,

transaction_date DATE,

amfi_code TEXT,

transaction_type TEXT,

amount_inr REAL

);

CREATE TABLE fact_performance(

amfi_code TEXT,

return_1yr_pct REAL,

return_3yr_pct REAL,

return_5yr_pct REAL,

sharpe_ratio REAL,

sortino_ratio REAL,

alpha REAL,

beta REAL

);

