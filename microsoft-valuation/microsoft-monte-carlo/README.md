# Monte Carlo Simulation

This is my final project for Harvard's CS50P course.
I will build a Monte Carlo Simulation of the DCF Valuation Model of Microsoft Corporation (Ticker: MSFT) I had already made in Excel, instead in Python.
I documented the entire process below.

## Requirements by CS50P
1. Your project must be implemented in Python.
2. Your project must have a main function and three or more additional functions. At least three of those additional functions must be accompanied by tests that can be executed with `pytest`.
    - Your main function must be in a file called `project.py`, which should be in the “root” (i.e., top-level folder) of your project.
    - Your 3 required custom functions other than main must also be in `project.py` and defined at the same indentation level as main (i.e., not nested under any classes or functions).
    - Your test functions must be in a file called `test_project.py`, which should also be in the “root” of your project. Be sure they have the same name as your custom functions, prepended with test_ (`test_custom_function`, for example, where `custom_function` is a function you’ve implemented in `project.py`).
3. You are welcome to implement additional classes and functions as you see fit beyond the minimum requirement.
4. Any pip-installable libraries that your project requires must be listed, one per line, in a file called `requirements.txt` in the root of your project. This file allows others to install your project’s dependencies with `pip install -r requirements.txt`.

# Introduction and how the code should function:

The DCF Model on Excel computes the implied share price of MSFT using values such as projected revenue,
projected free cash flows, and WACC. However, a number of these values (and the values used in their 
intermediate workings) are fixed and uncertain assumptions. The goal of this code is to replace these 
uncertain values with a range of values around the original value, run the DCF Valuation using a random
number in range for all those ranges, repeat that 1000 times, and finally output a distribution of all
possible results to see which implied share price is the average.

# Building the Python code:

## Step 1: Determine which variables are uncertain
Since the DCF Model in Excel is mainly formula-driven, I should look at the hardcoded values with the most impact.
I decided to replace the following uncertain assumptions with ranges to be randomly-sampled from later on:
>    1. Revenue growth rate (%): Most impactful uncertain assumption as most values are derived from projected revenue. How much the growth decreases YOY after FY26 is an assumption I made due to normalising Azure capacity.  
>    2. Cost of Revenue (as % of Revenue): The next biggest uncertain assumption that directly impacts operating profit. I made the assumption that gross margin rates would decrease (i.e. for same $ of revenue, more costs are incurred) because of increasing AI infrastructure investments.  
>    3. WACC (%): The highest weightage in WACC is the Cost of Equity (Risk Free Rate + Beta*(Equity Risk Premium)) at 96%. This means it is more efficient to randomize WACC as a whole directly instead of the 3 intermediate values independently, as the cost of debt is immaterial in this case.  
>    4. Terminal Growth Rate (%): Used to calculate Terminal Value at the last projected year (FY31). Not only does Terminal Value make up the biggest portion of Enterprise Value (which is used to calculate implied share price), I also assumed Terminal Value using a mix of Real GDP Growth and PCE Inflation which is not constant, hence the rate should be randomized.

## Step 2: Method to extract data and formulas from Microsoft Excel (.xlsx) file
The 2 most prominent libraries that appeared in Google searches were `openpyxl` and `xlwings`.

`xlwings` opens an instance of Excel and hence requires the user to have a local copy, but can read live cell data.

`openpyxl` can extract data from a file url using the `io` library, which doesn't require the user to have a local copy.

## Step 3: Define each function and what they should do
1. main():
2. calculate_fcf():
3. calculate_wacc():
4. 
