"""
Summary statistics, distribution plot, and variance-contribution ranking
for the Monte Carlo simulation results.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import spearmanr

ACTUAL_PRICE = 373.02  # MSFT close, June 30, 2026 (valuation date)


def summarize(df: pd.DataFrame, actual_price=ACTUAL_PRICE) -> dict:
    prices = df["implied_price"]
    return {
        "n_iterations": len(prices),
        "mean": prices.mean(),
        "median": prices.median(),
        "std_dev": prices.std(),
        "p5": prices.quantile(0.05),
        "p25": prices.quantile(0.25),
        "p75": prices.quantile(0.75),
        "p95": prices.quantile(0.95),
        "prob_undervalued": (prices > actual_price).mean(),  # P(model implies MSFT is worth more than market price)
    }


def print_summary(summary: dict):
    print("=" * 55)
    print("MONTE CARLO DCF — MSFT SUMMARY")
    print("=" * 55)
    print(f"Iterations:              {summary['n_iterations']:,}")
    print(f"Mean implied price:      ${summary['mean']:,.2f}")
    print(f"Median implied price:    ${summary['median']:,.2f}")
    print(f"Std deviation:           ${summary['std_dev']:,.2f}")
    print(f"5th percentile:          ${summary['p5']:,.2f}")
    print(f"25th percentile:         ${summary['p25']:,.2f}")
    print(f"75th percentile:         ${summary['p75']:,.2f}")
    print(f"95th percentile:         ${summary['p95']:,.2f}")
    print(f"Actual market price:     ${ACTUAL_PRICE:,.2f}")
    print(f"P(model implies undervalued at market price): {summary['prob_undervalued']:.1%}")
    print("=" * 55)


def plot_distribution(df: pd.DataFrame, actual_price=ACTUAL_PRICE, save_path="../outputs/distribution.png"):
    prices = df["implied_price"]
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(prices, bins=80, color="#1F4E78", alpha=0.75, edgecolor="white")
    ax.axvline(actual_price, color="#C0392B", linestyle="--", linewidth=2,
               label=f"Market Price (${actual_price:,.2f})")
    ax.axvline(prices.median(), color="black", linestyle="-", linewidth=2,
               label=f"Median Implied Value (${prices.median():,.0f})")
    ax.set_xlabel("Implied Share Price ($)")
    ax.set_ylabel("Frequency")
    ax.set_title(f"Monte Carlo DCF: Distribution of Implied MSFT Share Price (n={len(prices):,})")
    ax.legend()
    plt.tight_layout()
    plt.savefig(save_path, dpi=150)
    print(f"Saved distribution chart to {save_path}")
    plt.close(fig)


def variance_contribution(df: pd.DataFrame) -> pd.Series:
    """Spearman rank correlation between each sampled input and the output price.
    Larger |correlation| = that input explains more of the variation in output."""
    input_cols = [c for c in df.columns if c != "implied_price"]
    correlations = {}
    for col in input_cols:
        corr, _ = spearmanr(df[col], df["implied_price"])
        correlations[col] = corr
    return pd.Series(correlations).sort_values(key=np.abs, ascending=False)


def plot_tornado(corr_series: pd.Series, save_path="../outputs/tornado_chart.png"):
    fig, ax = plt.subplots(figsize=(9, 6))
    corr_sorted = corr_series.sort_values()
    colors = ["#C0392B" if v < 0 else "#1F4E78" for v in corr_sorted.values]
    ax.barh(corr_sorted.index, corr_sorted.values, color=colors)
    ax.set_xlabel("Spearman Correlation with Implied Share Price")
    ax.set_title("Which Assumptions Drive the Valuation? (Variance Contribution)")
    ax.axvline(0, color="black", linewidth=0.8)
    plt.tight_layout()
    plt.savefig(save_path, dpi=150)
    print(f"Saved tornado chart to {save_path}")
    plt.close(fig)


if __name__ == "__main__":
    df = pd.read_csv("../outputs/simulation_results.csv")

    summary = summarize(df)
    print_summary(summary)

    plot_distribution(df)

    corr = variance_contribution(df)
    print("\nVariance contribution ranking (most to least influential):")
    print(corr)
    plot_tornado(corr)
