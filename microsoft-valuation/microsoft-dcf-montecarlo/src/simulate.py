"""
Runs the Monte Carlo simulation: draws N random input sets, runs the DCF
for each, and stores both the resulting price and the sampled inputs
(the latter needed later for sensitivity/variance-contribution analysis).
"""

import numpy as np
import pandas as pd
from model import run_dcf
from distributions import sample_inputs


def run_simulation(n=10000, seed=42):
    rng = np.random.default_rng(seed)

    prices = np.empty(n)
    input_records = []

    for i in range(n):
        inputs = sample_inputs(rng)
        prices[i] = run_dcf(**inputs)

        # Flatten tuple-valued inputs (e.g. rev_growth path) down to a single
        # representative scalar per input, for the variance-contribution step.
        record = {
            "rev_growth_y1": inputs["rev_growth"][0],
            "rev_growth_y5": inputs["rev_growth"][-1],
            "cogs_pct_y5": inputs["cogs_pct"][-1],
            "rd_pct_y5": inputs["rd_pct"][-1],
            "sm_growth_y1": inputs["sm_growth"][0],
            "ga_growth_y1": inputs["ga_growth"][0],
            "tax_rate_y5": inputs["tax_rate"][-1],
            "capex_pct_y1": inputs["capex_pct"][0],
            "useful_life": inputs["useful_life"],
            "nwc_pct": inputs["nwc_pct"],
            "wacc": inputs["wacc"],
            "terminal_growth": inputs["terminal_growth"],
            "net_debt": inputs["net_debt"],
        }
        input_records.append(record)

    results_df = pd.DataFrame(input_records)
    results_df["implied_price"] = prices

    return results_df


if __name__ == "__main__":
    df = run_simulation(n=10000, seed=42)
    df.to_csv("../outputs/simulation_results.csv", index=False)
    print(df["implied_price"].describe())
    print(f"\nSaved {len(df):,} iterations to outputs/simulation_results.csv")
