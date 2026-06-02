SELECT *
FROM fact_performance
ORDER BY return_3yr_pct DESC
LIMIT 5;

SELECT AVG(nav) AS avg_nav
FROM fact_nav;

SELECT MIN(nav) AS min_nav
FROM fact_nav;

SELECT MAX(nav) AS max_nav
FROM fact_nav;

SELECT
scheme_name,
expense_ratio_pct
FROM dim_fund
WHERE expense_ratio_pct < 1;

SELECT
category,
COUNT(*) AS total_funds
FROM dim_fund
GROUP BY category;

SELECT
state,
COUNT(*) AS total_transactions
FROM fact_transactions
GROUP BY state
ORDER BY total_transactions DESC;

SELECT
state,
SUM(amount_inr) AS total_amount
FROM fact_transactions
GROUP BY state
ORDER BY total_amount DESC;

SELECT
transaction_type,
COUNT(*) AS total
FROM fact_transactions
GROUP BY transaction_type;

SELECT
investor_id,
SUM(amount_inr) AS total_invested
FROM fact_transactions
GROUP BY investor_id
ORDER BY total_invested DESC
LIMIT 10;