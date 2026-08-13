# Microsoft (MSFT) — Monte Carlo DCF Valuation

**Part 2** of a two-part valuation project. Part 1 built a full deterministic
DCF for Microsoft from the FY2026 10-K (see companion repo/report), producing
a single implied share price of **$293.08** against an actual market price of
**$373.02** as at the June 30, 2026 valuation date.

A single point estimate implicitly overstates precision — every input feeding
it (WACC, terminal growth, revenue growth, CapEx trajectory, useful life, tax
rate) is a judgment call with genuine uncertainty. This project replaces each
key deterministic assumption with a probability distribution and runs 10,000
simulations to produce a full distribution of plausible outcomes, rather than
one number.

## Results (n = 10,000, seed = 42)

| Metric | Value |
|---|---|
| Median implied price | $300.06 |
| Mean implied price | $307.27 |
| Std deviation | $61.47 |
| 5th percentile | $220.01 |
| 95th percentile | $418.35 |
| Actual market price (6/30/26) | $373.02 |
| **P(model implies MSFT is undervalued at market price)** | **13.5%** |

The distribution is right-skewed, which is expected given the Gordon Growth
terminal value formula's sensitivity as WACC approaches the terminal growth
rate in a subset of draws.

**Variance contribution** (which assumptions actually drive the output,
ranked by Spearman correlation with implied price): **WACC** and **near-term
CapEx intensity** dominate — far more than revenue growth assumptions. This
validates that the deepest analytical effort in the original deterministic
build (WACC construction from Microsoft's actual capital structure; CapEx
anchored to disclosed guidance rather than a historical average) was placed
on the inputs that matter most to the final valuation.

## Methodology

- **Deterministic base:** `src/model.py` is a faithful line-by-line port of
  the original Excel DCF (revenue build → operating profit → NOPAT → FCF via
  a PP&E roll-forward for D&A → mid-year discounting → Gordon Growth terminal
  value → equity bridge). Calling `run_dcf()` with no arguments reproduces
  the original Excel model's $293.08 output exactly — this is the validation
  checkpoint that confirms the Python port is correct before any
  randomization is introduced.
- **Randomization:** rather than independently randomizing every year-by-year
  cell (which would understate real uncertainty through artificial
  diversification), most multi-year assumption paths are perturbed via a
  single "regime shock" applied consistently across all five forecast years
  — e.g., if COGS margin pressure is worse than the base case, it's modeled
  as worse across the whole forecast window, not randomly different each
  year. See `src/distributions.py` for the full distribution definitions and
  the reasoning behind each one's shape (triangular vs. normal) and
  parameters.
- **Simulation:** `src/simulate.py` draws 10,000 independent input sets and
  runs the full DCF for each, storing both the resulting price and the
  sampled inputs.
- **Analysis:** `src/analyze.py` produces summary statistics, a distribution
  histogram, and a variance-contribution ("tornado") ranking via Spearman
  rank correlation between each input and the output.

## Repo structure

```
├── data/
│   └── assumptions.json       # deterministic base-case point estimates
├── src/
│   ├── model.py                # deterministic DCF as a function
│   ├── distributions.py        # probability distribution for each input
│   ├── simulate.py             # Monte Carlo loop
│   └── analyze.py              # summary stats, plots, variance ranking
├── notebooks/
│   └── monte_carlo_dcf.ipynb   # walkthrough notebook, run this end-to-end
├── outputs/
│   ├── simulation_results.csv
│   ├── distribution.png
│   └── tornado_chart.png
└── requirements.txt
```

## Running it

```bash
pip install -r requirements.txt
cd src
python simulate.py   # runs the simulation, writes outputs/simulation_results.csv
python analyze.py    # prints summary stats, writes distribution.png and tornado_chart.png
```

Or open `notebooks/monte_carlo_dcf.ipynb` for the full walkthrough with
inline output.

## Data sources

All base-case point estimates each distribution is centered on trace back to
the original deterministic DCF's assumptions register — Microsoft's FY2026
Form 10-K, company guidance, Yahoo Finance, Aswath Damodaran's equity risk
premium data, and the Federal Reserve's June 2026 Summary of Economic
Projections. See `data/assumptions.json` for the full point-estimate record.

## Limitations

- Distribution shapes and parameters (especially standard deviations) are
  reasoned estimates, not derived from historical time-series volatility —
  stated explicitly in `src/distributions.py`'s comments.
- Some correlation between inputs that would exist in reality (e.g., a lower
  WACC environment plausibly coinciding with a higher terminal growth
  environment) is not modeled — each input is currently drawn independently.
- This is a probabilistic *illustration* of uncertainty around a single
  analyst's assumptions, not a claim about the "true" probability
  distribution of Microsoft's future value.
