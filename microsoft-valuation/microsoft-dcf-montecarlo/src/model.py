"""
This file is a Python port of the Microsoft DCF model originally built in Excel.
The run_dcf() function, with no arguments, should exactly  reproduce the Excel
model's output of approximately $293.08 implied share price.
"""

# Load NumPy library for numerical operations
import numpy as np

# Define the run_dcf function to perform the DCF with original values in the Excel model
def run_dcf(
    # --- Revenue ---
    revenue_fy26=331839,                                         # Disclosed FY26 revenue from 10-K, in millions
    rev_growth=(0.18, 0.15, 0.125, 0.105, 0.09),                 # FY27-FY31 growth rates, in decimal form

    # --- Cost of Revenue / R&D (% of revenue) ---
    cogs_pct=(0.325, 0.329, 0.332, 0.334, 0.336),                # Cost of Revenue from FY27-FY31, in decimal form
    rd_pct=(0.103, 0.10, 0.098, 0.096, 0.094),                   # R&D from FY27-FY31, in decimal form

    # --- S&M / G&A (dollar growth rate, off FY26 base) ---
    sm_fy26=26710,                                               # Disclosed FY26 S&M from 10-K, in millions
    sm_growth=(0.041, 0.04, 0.0292, 0.0282, 0.0282),             # FY27-FY31 growth rates, in decimal form
    ga_fy26=7956,                                                # Disclosed FY26 G&A from 10-K, in millions                                       
    ga_growth=(0.032, 0.032, 0.0222, 0.0222, 0.0222),            # FY27-FY31 growth rates, in decimal form

    # --- Tax ---
    tax_rate=(0.196, 0.198, 0.20, 0.201, 0.202),                 # Effective tax rates projected to FY27-FY31, in decimal form of percentages

    # --- CapEx (% of revenue) ---
    capex_pct=(0.44691879117813976, 0.42, 0.403, 0.388, 0.378),  # CapEx as a percentage of revenue, projected to FY27-FY31, in decimal form.

    # --- D&A / PP&E rollforward ---
    opening_ppe_fy27=313076,
    useful_life=5.98,

    # --- NWC ---
    nwc_fy26_actual=-48331,
    nwc_pct=-0.1415559085913948,   # applied flat across FY27-31

    # --- WACC / Terminal Value ---
    wacc=0.09485115129674662,
    terminal_growth=0.04,

    # --- Bridge to equity value ---
    net_debt=82159,
    shares=7427,

    return_detail=False,
):
    n = 5  # explicit forecast years, FY27-FY31

    # ---- Revenue build ----
    revenue = [revenue_fy26]
    for g in rev_growth:
        revenue.append(revenue[-1] * (1 + g))
    revenue_fy = revenue[1:]  # FY27..FY31

    # ---- S&M / G&A dollar build ----
    sm = [sm_fy26]
    for g in sm_growth:
        sm.append(sm[-1] * (1 + g))
    sm_fy = sm[1:]

    ga = [ga_fy26]
    for g in ga_growth:
        ga.append(ga[-1] * (1 + g))
    ga_fy = ga[1:]

    # ---- Operating profit ----
    op_profit = []
    for i in range(n):
        gross_margin = revenue_fy[i] * (1 - cogs_pct[i])
        rd = revenue_fy[i] * rd_pct[i]
        op = gross_margin - rd - sm_fy[i] - ga_fy[i]
        op_profit.append(op)

    # ---- Taxes / NOPAT ----
    taxes = [op_profit[i] * tax_rate[i] for i in range(n)]
    nopat = [op_profit[i] - taxes[i] for i in range(n)]

    # ---- CapEx ----
    capex = [revenue_fy[i] * capex_pct[i] for i in range(n)]

    # ---- D&A / PP&E rollforward ----
    da = []
    ppe = opening_ppe_fy27
    for i in range(n):
        d = ppe / useful_life
        da.append(d)
        ppe = ppe + capex[i] - d

    # ---- NWC ----
    nwc_series = [nwc_fy26_actual] + [revenue_fy[i] * nwc_pct for i in range(n)]
    nwc_adjustment = [nwc_series[i] - nwc_series[i + 1] for i in range(n)]

    # ---- Unlevered FCF ----
    fcf = [nopat[i] + da[i] - capex[i] + nwc_adjustment[i] for i in range(n)]

    # ---- Discounting (mid-year convention) ----
    pv_fcf = [fcf[i] / (1 + wacc) ** (i + 0.5) for i in range(n)]

    # ---- Terminal value ----
    tv = fcf[-1] * (1 + terminal_growth) / (wacc - terminal_growth)
    pv_tv = tv / (1 + wacc) ** (n - 0.5)

    enterprise_value = sum(pv_fcf) + pv_tv
    equity_value = enterprise_value - net_debt
    implied_price = equity_value / shares

    if return_detail:
        return {
            "revenue_fy": revenue_fy,
            "op_profit": op_profit,
            "nopat": nopat,
            "capex": capex,
            "da": da,
            "nwc_adjustment": nwc_adjustment,
            "fcf": fcf,
            "pv_fcf": pv_fcf,
            "terminal_value": tv,
            "pv_terminal_value": pv_tv,
            "enterprise_value": enterprise_value,
            "equity_value": equity_value,
            "implied_price": implied_price,
        }

    return implied_price


if __name__ == "__main__":
    price = run_dcf()
    print(f"Implied share price (base case): ${price:,.2f}")
