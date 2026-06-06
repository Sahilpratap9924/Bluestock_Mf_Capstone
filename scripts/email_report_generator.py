from pathlib import Path
import pandas as pd
import webbrowser

root_dir = Path(__file__).resolve().parent.parent
input_path = root_dir / "data" / "processed" / "fund_scorecard.csv"
out_path = root_dir / "reports" / "weekly_report.html"

scorecard = pd.read_csv(input_path)

top5 = scorecard.sort_values(
    "composite_score",
    ascending=False
).head(5)

html_content = f"""
<html>
<head>
<title>Weekly Performance Report</title>
</head>

<body>

<h1>Weekly Mutual Fund Performance Summary</h1>

<h2>Top 5 Funds</h2>

{top5.to_html(index=False)}

</body>
</html>
"""

out_path.parent.mkdir(parents=True, exist_ok=True)
with out_path.open("w", encoding="utf-8") as f:
    f.write(html_content)

print(f"HTML report generated successfully: {out_path}")
import webbrowser

webbrowser.open(out_path.as_uri())