# Bitcoin Live Price Tracker

This program converts a specified number of Bitcoin (BTC) into 
its value in USD using live exchange rates from CoinCap. 
Based off Harvard's CS50 Python Problem Set 4. Code written 
was submitted and accepted by CS50's check50 program. 

## Requirements
- Python 3
- Installation of requests library ("pip install requests" in terminal)
- A valid CoinCap API Key (create own account on CoinCap)

## How to use
1. Make sure you are in the correct directory with cd (folder_name).
2. Run the script in the terminal with python bitcoin.py (number of BTC).
3. Number of BTC must be an integer or a float. If argument cannot be converted to float, system will exit.
4. Program will output the live total price of the number of BTC specified in USD and to 4 decimal places.

## How it works
- Imports sys for runtime environment manipulation and command-line argument parsing.
- Imports requests to handle synchronous HTTP networking.
- Executes a blocking GET request to the CoinCap REST API endpoint.
- Deserializes the JSON response payload into a native Python dictionary (data).
- Initializes an infinite while True loop to continuously poll logic execution until broken.
- Pulls the first element ([1]) from the CLI argument array (sys.argv) into a string variable.
- Evaluates input with .isalpha() to check if the string contains only alphabetic characters. If input has alphabetic characters, triggers the else block and terminates runtime immediately via sys.exit().
- Branches logic based on the boolean result.
- Creates try block: Attempts to cast the input string into a float numeric type (float()), multiplies the casted user input with the nested "priceUsd" float value pulled from the API dataset, prints the resulting value formatted explicitly to 4 decimal places via an f-string if successful, and breaks the loop.
- except ValueError block: Catches casting failures (e.g., special characters) and terminates runtime immediately via sys.exit().
