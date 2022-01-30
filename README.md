# smithwilson
## Overview
This Python package implements the Smith-Wilson yield curve fitting algorithm. It allows for interpolations and extrapolations of zero-coupon bond rates. This algorithm is used for the extrapolation of [EIOPA risk-free term structures](https://eiopa.europa.eu/Publications/Standards/Technical%20Documentation%20(31%20Jan%202018).pdf) in the Solvency II framework. Details are available in the Technical Paper [QIS 5  Risk-free interest rates](https://eiopa.europa.eu/Publications/QIS/ceiops-paper-extrapolation-risk-free-rates_en-20100802.pdf). Examples of extrapolated yield curves including the parameters applied can be found [here](https://eiopa.europa.eu/Publications/Standards/EIOPA_RFR_20190531.zip).
<br /><br />

## How to use the package
1. Install the package with `pip install smithwilson`
2. To use the Smith-Wilson fitting algorithm, first import the Python package and specify the inputs. In the example below the inputs are zero-coupon rates with annual frequency up until year 25. The UFR is 2.9% and the convergence parameter alpha is 0.128562. The `terms` list defines the list of maturities, in this case `[1.0, 2.0, 3.0, ..., 25.0]`
    ```py
    import smithwilson as sw

    # Input - Switzerland EIOPA spot rates with LLP of 25 years
    # Source: https://eiopa.europa.eu/Publications/Standards/EIOPA_RFR_20190531.zip
    #         EIOPA_RFR_20190531_Term_Structures.xlsx; Tab: RFR_spot_no_VA
    rates = [-0.00803, -0.00814, -0.00778, -0.00725, -0.00652,
             -0.00565, -0.0048, -0.00391, -0.00313, -0.00214,
             -0.0014, -0.00067, -0.00008, 0.00051, 0.00108,
             0.00157, 0.00197, 0.00228, 0.0025, 0.00264,
             0.00271, 0.00274, 0.0028, 0.00291, 0.00309]
    terms = [float(y + 1) for y in range(len(rates))] # [1.0, 2.0, ..., 25.0]
    ufr = 0.029
    alpha = 0.128562

    ```

3. Specify the targeted output maturities. This is the set of terms you want to get rates fitted by Smith-Wilson.
   Expand the set of rates beyond the Last Liquid Point (e.g. extrapolate to 150 years with annual frequency):
   ```py
   # Extrapolate to 150 years
   terms_target = [float(y + 1) for y in range(150)] # [1.0, 2.0, ..., 150.0]
   ```

   Alternatively, you can retrieve a different frequency (e.g. interpolate quarterly instead of annual):
   ```py
   # Interpolate to quarterly granularity
   terms_target = [float(y + 1) / 4 for y in range(25*4)] # [0.25, 0.5, ..., 25.0]
   ```

   A combination of interpolation & extrapolation is possible, too. Same for sets of arbitrary maturities:
   ```py
   # Get rates for a well-specified set of maturities only
   terms_target = [0.25, 0.5, 1.0, 2.0, 5.0, 10.0, 20.0, 50.0, 100.0]
   ```

4. Call the Smiwth-Wilson fitting algorithm. This returns the rates as numpy vector with each element corresponding to the maturity in `terms_target`
   ```py
   # Calculate fitted rates based on actual observations and two parametes alpha & UFR
   fitted_rates = sw.fit_smithwilson_rates(rates_obs=rates, t_obs=terms,
                                           t_target=terms_target, ufr=ufr,
                                           alpha=alpha)  # Optional
   ```

   The convergence parameter alpha is optional and will be estimated if not provided. The parameter determines the convergence speed of the yield curve towards the Ultimate Forward Rate (UFR). The parameter is estimated by finding the smallest value such that the difference between forward rate at convergence maturity and UFR is smaller than 1bps.

5. To display the results and/or processing them it can be useful to turn them into a table, here using the pandas library:
   ```py
   # Ensure pandas package is imported
   import pandas as pd

   # ...

   # Turn inputs & outputs into dataframe
   observed_df = pd.DataFrame(data=rates, index=terms, columns=["observed"])
   extrapolated_df = pd.DataFrame(data=fitted_rates, index=terms_target, columns=["extrapolated"])

   # Combine and print dataframe
   print(observed_df.join(extrapolated_df, how="outer"))
   ```

A complete example can be found in [main.py](https://github.com/simicd/smith-wilson-py/blob/master/main.py)
<br /><br />

## Algorithm
The algorithm is fully vectorized and uses numpy, making it very performant. The code is in [core.py](https://github.com/simicd/smith-wilson-py/blob/master/smithwilson/core.py).

The function `fit_smithwilson_rates()` expects following parameters:
- Observed rates
- Observed maturities
- Target maturities
- Convergence parameter alpha
- Ultimate forward rate (UFR)

The observed rates and maturities are assumed to be before the Last Liquid Point (LLP). The targeted maturity vector can
contain any set of maturities (e.g. more granular maturity structure (interpolation) or terms after the LLP (extrapolation)).
<br /><br />


The Smith-Wilson fitting algorithm calculates first the Wilson-matrix (EIOPA, 2010, p. 16):

    W = e^(-UFR * (t1 + t2)) * (α * min(t1, t2) - 0.5 * e^(-α * max(t1, t2))
        * (e^(α * min(t1, t2)) - e^(-α * min(t1, t2))))

Given the Wilson-matrix `W`, vector of UFR discount factors `μ` and prices `P`, the parameter vector `ζ` can be calculated as follows (EIOPA, 2010, p.17):

    ζ = W^-1 * (μ - P)

With the Smith-Wilson parameter `ζ` and Wilson-matrix `W`, the zero-coupon bond prices can be represented as (EIOPA, 2010, p. 18) in matrix notation:

    P = e^(-t * UFR) - W * ζ

In the last case, `t` can be any maturity vector, i.e. with additional maturities to extrapolate rates.
<br /><br />

## Sources
[EIOPA (2010). QIS 5 Technical Paper; Risk-free interest rates – Extrapolation method](https://eiopa.europa.eu/Publications/QIS/ceiops-paper-extrapolation-risk-free-rates_en-20100802.pdf); p.11ff

[EIOPA (2018). Technical documentation of the methodology to derive EIOPA’srisk-free interest rate term structures](https://eiopa.europa.eu/Publications/Standards/Technical%20Documentation%20(31%20Jan%202018).pdf); p.37-46
<br /><br />
