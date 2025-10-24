def dcf(CF0, g_CAGR, g_GDP, r=0.10, sustainable_growth=0.02, years=10):
    CF = []
    for t in range(1, years + 1):
        if t <= 5:
            CF_t = CF0 * (1 + g_CAGR)**t
        else:
            CF_t = CF0 * (1 + g_CAGR)**5 * (1 + g_GDP)**(t - 5)
        CF.append(CF_t)

    # present value of each year
    PV = [cf / (1 + r)**t for t, cf in enumerate(CF, start=1)]

    # terminal value and its present value
    CF10 = CF[-1]
    TV = CF10 * (1 + sustainable_growth) / (r - sustainable_growth)
    PV_TV = TV / (1 + r)**10

    PV_total = sum(PV) + PV_TV

    import pandas as pd
    df = pd.DataFrame({
        "Year": range(1, years + 1),
        "Cash Flow": [round(cf, 2) for cf in CF],
        "PV Each Year": [round(pv, 2) for pv in PV]
    })

    print(df)
    print("\nTerminal Value:", round(TV, 2))
    print("PV of Terminal Value:", round(PV_TV, 2))
    print("Total Fair Value (per share):", round(PV_total, 2))

    return df, PV_total

# Example: 優群 3217 CF0=14.29, CAGR=23.7%, GDP=3%
dcf(14.29, 0.237, 0.03, 0.10, 0.02)
