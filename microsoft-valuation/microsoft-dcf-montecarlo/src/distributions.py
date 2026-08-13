"""
Defines probability distributions for the uncertain DCF inputs and converts
each random draw into the full set of keyword arguments run_dcf() expects.

Design choice: rather than randomizing each of the ~25 individual year-by-year
cells independently (which would understate real uncertainty via diversification
that doesn't exist in reality), most line items are perturbed via a single
"regime shock" applied consistently across all 5 forecast years. If COGS margin
pressure turns out worse than expected, it's reasonable to assume it's worse
across the whole forecast window, not randomly different each year.
"""

import numpy as np

# Base-case paths, taken directly from the Excel model (src/model.py defaults)
BASE_COGS_PCT = np.array([0.325, 0.329, 0.332, 0.334, 0.336])
BASE_RD_PCT = np.array([0.103, 0.10, 0.098, 0.096, 0.094])
BASE_SM_GROWTH = np.array([0.041, 0.04, 0.0292, 0.0282, 0.0282])
BASE_GA_GROWTH = np.array([0.032, 0.032, 0.0222, 0.0222, 0.0222])
BASE_TAX_RATE = np.array([0.196, 0.198, 0.20, 0.201, 0.202])
BASE_CAPEX_PCT = np.array([0.44691879117813976, 0.42, 0.403, 0.388, 0.378])


def sample_inputs(rng: np.random.Generator) -> dict:
    """Draw one full set of random model inputs, ready to unpack into run_dcf()."""

    # --- Revenue growth: randomize the taper endpoints, interpolate between ---
    g_y1 = rng.triangular(0.14, 0.18, 0.20)   # FY27 growth
    g_y5 = rng.triangular(0.06, 0.09, 0.12)   # FY31 growth
    rev_growth = tuple(np.linspace(g_y1, g_y5, 5))

    # --- Margin/expense paths: single regime shock applied across all 5 years ---
    cogs_shift = rng.normal(0, 0.010)
    cogs_pct = tuple(np.clip(BASE_COGS_PCT + cogs_shift, 0.20, 0.45))

    rd_shift = rng.normal(0, 0.006)
    rd_pct = tuple(np.clip(BASE_RD_PCT + rd_shift, 0.06, 0.16))

    sm_shift = rng.normal(0, 0.008)
    sm_growth = tuple(BASE_SM_GROWTH + sm_shift)

    ga_shift = rng.normal(0, 0.010)
    ga_growth = tuple(BASE_GA_GROWTH + ga_shift)

    tax_shift = rng.normal(0, 0.008)
    tax_rate = tuple(np.clip(BASE_TAX_RATE + tax_shift, 0.10, 0.28))

    # --- CapEx: scale the whole path by one multiplicative factor ---
    capex_scale = rng.normal(1.0, 0.08)
    capex_pct = tuple(np.clip(BASE_CAPEX_PCT * capex_scale, 0.20, 0.65))

    # --- D&A useful life ---
    useful_life = rng.triangular(4.5, 5.98, 7.0)

    # --- NWC ---
    nwc_pct = rng.normal(-0.1415559085913948, 0.010)

    # --- WACC ---
    wacc = max(rng.normal(0.09485115129674662, 0.007), 0.03)  # floor to avoid nonsense values

    # --- Terminal growth ---
    terminal_growth = rng.triangular(0.03, 0.04, 0.05)
    # Safety: terminal growth must stay comfortably below WACC or the Gordon
    # Growth formula explodes/goes negative. Cap it if a rare draw violates this.
    terminal_growth = min(terminal_growth, wacc - 0.02)

    # --- Net debt (minor data/timing uncertainty) ---
    net_debt = rng.normal(82159, 3000)

    return dict(
        rev_growth=rev_growth,
        cogs_pct=cogs_pct,
        rd_pct=rd_pct,
        sm_growth=sm_growth,
        ga_growth=ga_growth,
        tax_rate=tax_rate,
        capex_pct=capex_pct,
        useful_life=useful_life,
        nwc_pct=nwc_pct,
        wacc=wacc,
        terminal_growth=terminal_growth,
        net_debt=net_debt,
    )
