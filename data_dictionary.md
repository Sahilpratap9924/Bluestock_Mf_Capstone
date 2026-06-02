# dim_fund

| Column | Type | Description |
|----------|----------|----------|
| amfi_code | TEXT | Unique AMFI scheme code |
| scheme_name | TEXT | Mutual fund scheme name |
| fund_house | TEXT | AMC name |
| category | TEXT | Equity/Debt/Hybrid |
| sub_category | TEXT | Large Cap/Mid Cap/etc |
| expense_ratio_pct | REAL | Expense ratio percentage |
| risk_category | TEXT | Risk level |

# fact_nav

| Column | Type | Description |
|----------|----------|----------|
| amfi_code | TEXT | Fund identifier |
| date | DATE | NAV date |
| nav | REAL | Net Asset Value |
| daily_return | REAL | Daily return percentage |

# fact_transactions

| Column | Type | Description |
|----------|----------|----------|
| investor_id | TEXT | Investor identifier |
| transaction_date | DATE | Transaction date |
| amfi_code | TEXT | Fund code |
| transaction_type | TEXT | SIP/Lumpsum/Redemption |
| amount_inr | REAL | Transaction amount |
| state | TEXT | Investor state |
| city | TEXT | Investor city |
| age_group | TEXT | Investor age group |
| kyc_status | TEXT | Verification status |

# fact_performance

| Column | Type | Description |
|----------|----------|----------|
| return_1yr_pct | REAL | 1-year return |
| return_3yr_pct | REAL | 3-year return |
| return_5yr_pct | REAL | 5-year return |
| sharpe_ratio | REAL | Sharpe ratio |
| sortino_ratio | REAL | Sortino ratio |
| alpha | REAL | Alpha |
| beta | REAL | Beta |

