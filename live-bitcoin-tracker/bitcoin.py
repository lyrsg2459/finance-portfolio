import sys
import requests

response = requests.get("https://rest.coincap.io/v3/assets/bitcoin?apiKey=072bb9640cf7d91066cf9f9a7e11210344e56a83d0cf8400f4b571e4ccded507")
data = response.json()

while True:
    number_str = sys.argv[1]

    if not number_str.isalpha():

        try:
            number = float(number_str)
            amount = number * float(data["data"]["priceUsd"])
            print(f"${amount:,.4f}")
            break

        except ValueError:
            sys.exit("Missing command-line argument")

    else:
        sys.exit("Command-line argument is not a number")
