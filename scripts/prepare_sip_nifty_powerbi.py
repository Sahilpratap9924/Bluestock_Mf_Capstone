"""
Script to merge SIP Inflows with Nifty 50 index data for Power BI visualization
Creates a combined CSV with monthly SIP inflows and month-end Nifty 50 values
"""

import pandas as pd
from datetime import datetime

# Load data
sip_df = pd.read_csv('data/raw/04_monthly_sip_inflows.csv')
nifty_df = pd.read_csv('data/raw/10_benchmark_indices.csv')

# Convert date columns
nifty_df['date'] = pd.to_datetime(nifty_df['date'])

# Filter for Nifty 50 only
nifty_50 = nifty_df[nifty_df['index_name'] == 'NIFTY50'].copy()

# Get month-end Nifty 50 values
nifty_50['year_month'] = nifty_50['date'].dt.to_period('M')
nifty_monthly = nifty_50.sort_values('date').groupby('year_month').tail(1).copy()
nifty_monthly['month'] = nifty_monthly['year_month'].astype(str)
nifty_monthly = nifty_monthly[['month', 'close_value']].rename(columns={'close_value': 'nifty_50_index'})

# Parse SIP month to match format
sip_df['month'] = pd.to_datetime(sip_df['month']).dt.to_period('M').astype(str)

# Merge datasets
merged_df = sip_df.merge(nifty_monthly, on='month', how='left')

# Filter for 2022-2025
merged_df['year'] = merged_df['month'].str[:4].astype(int)
merged_df = merged_df[(merged_df['year'] >= 2022) & (merged_df['year'] <= 2025)]

# Sort by month
merged_df = merged_df.sort_values('month').reset_index(drop=True)

# Save to processed folder
merged_df.to_csv('data/processed/sip_nifty_trends.csv', index=False)

print("✓ File created: data/processed/sip_nifty_trends.csv")
print(f"\nData shape: {merged_df.shape}")
print(f"\nSample data:")
print(merged_df.head(10))
print(f"\nColumns: {list(merged_df.columns)}")
