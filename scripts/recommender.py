import pandas as pd


def load_data(
    scorecard_path="../data/processed/fund_scorecard.csv",
    master_path="../data/raw/01_fund_master.csv"
):
    scorecard = pd.read_csv(scorecard_path)
    master = pd.read_csv(master_path)
    return scorecard.merge(master, on="amfi_code")


def recommend(df, risk, top_n=3):
    result = (
        df[df["risk_category"] == risk]
          .sort_values("sharpe_ratio", ascending=False)
          .head(top_n)
    )
    return result[["scheme_name", "risk_category", "sharpe_ratio"]]


def save_recommendations(df, risk, output_path, top_n=3):
    recommendations = recommend(df, risk, top_n=top_n)
    recommendations.to_csv(output_path, index=False)
    return output_path


if __name__ == "__main__":
    df = load_data()
    output_file = save_recommendations(df, "High", "../scripts/recommendations_high.csv")
    print(f"Saved high-risk recommendations to: {output_file}")
