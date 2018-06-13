import csv
from dotenv import load_dotenv
import json
import os
import pdb
import requests
import datetime

def parse_response(response_text):
    # pdb.set_trace()
    # response_text can be either a raw JSON string or an already-converted dictionary
    if isinstance(response_text, str): # if not yet converted, then:
        response_text = json.loads(response_text) # convert string to dictionary

    results = []
    time_series_daily = response_text["Time Series (Daily)"] #> a nested dictionary
    for trading_date in time_series_daily: # FYI: can loop through a dictionary's top-level keys/attributes
        # pdb.set_trace()
        # print (trading_date)

        prices = time_series_daily[trading_date] #> {'1. open': '101.0924', '2. high': '101.9500', '3. low': '100.5400', '4. close': '101.6300', '5. volume': '22165128'}
        result = {
            "date": trading_date,
            "open": prices["1. open"],
            "high": prices["2. high"],
            "low": prices["3. low"],
            "close": prices["4. close"],
            "volume": prices["5. volume"]
        }
        results.append(result)
    return results

def write_prices_to_file(prices=[], filename="db/prices.csv"):
    csv_filepath = os.path.join(os.path.dirname(__file__), "..", filename)
    with open(csv_filepath, "w") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=["timestamp", "open", "high", "low", "close", "volume"])
        writer.writeheader()
        for d in prices:
            row = {
                "timestamp": d["date"], # change attribute name to match project requirements
                "open": d["open"],
                "high": d["high"],
                "low": d["low"],
                "close": d["close"],
                "volume": d["volume"]
            }
            writer.writerow(row)


if __name__ == '__main__': # only execute if file invoked from the command-line, not when imported into other files, like tests

    load_dotenv() # loads environment variables set in a ".env" file, including the value of the ALPHAVANTAGE_API_KEY variable

    api_key = os.environ.get("ALPHAVANTAGE_API_KEY") or "OOPS. Please set an environment variable named 'ALPHAVANTAGE_API_KEY'."
    print (api_key)
    # CAPTURE USER INPUTS (SYMBOL)

    symbol = input("Please input a stock symbol (e.g. 'NFLX'): ")

    # VALIDATE SYMBOL AND PREVENT UNECESSARY REQUESTS
    # pdb.set_trace()
    # converted_symbol = float(symbol)
    # if isinstance(response_text, float):
    #     print("Check your symbol. Expecting a Non-Numeric Symbol")
    #     quit()
    try:
        float(symbol)
        quit("Check your symbol. Expecting a Non-Numeric Symbol")
    except ValueError as e:
        pass

    # ASSEMBLE REQUEST URL
    # ... see: https://www.alphavantage.co/support/#api-key

    request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}"

    # ISSUE "GET" REQUEST

    response = requests.get(request_url)
    print(response.status_code)

    # VALIDATE RESPONSE AND HANDLE ERRORS
    if "Error Message" in response.text:
        print("REQUEST ERROR, PLEASE TRY AGAIN. CHECK YOUR STOCK SYMBOL.")
        quit("Stopping the program")

    # PARSE RESPONSE (AS LONG AS THERE ARE NO ERRORS)

    response_json = json.loads(response.text)
    # pdb.set_trace()

    daily_prices = parse_response(response.text)

    # WRITE TO CSV

    write_prices_to_file(prices=daily_prices, filename="db/prices.csv")

    # PERFORM CALCULATIONS
    # ... todo (HINT: use the daily_prices variable, and don't worry about the CSV file anymore :-)
    Latest_closing_price = daily_prices[0]["close"]
    Latest_closing_price  = float(Latest_closing_price)
    Latest_closing_price_usd = "{0:,.2f}".format(Latest_closing_price)

    print("Symbol: " + symbol)
    print("Processing Time: ", datetime.datetime.now().strftime("%Y-%m-%d %H:%m:%S"))
    Latest_available_day = daily_prices[0]["date"]
    print("Latest Data from: ", Latest_available_day)
    print("Latest_closing_price", Latest_closing_price_usd)


    array = []
    for item in daily_prices:
        array.append(item["high"])
    average_high_price = max(array)
    average_high_price  = float(average_high_price)
    average_high_price_usd = "{0:,.2f}".format(average_high_price)
    print ("average_high_price", average_high_price_usd)

    array = []
    for item in daily_prices:
        array.append(item["low"])
    average_low_price = min(array)
    average_low_price = float(average_low_price)
    average_low_price_usd = "{0:,.2f}".format(average_low_price)
    print ("average_low_price",average_low_price)


    # PRODUCE FINAL RECOMMENDATION
    Latest_low_price = daily_prices[0]["low"]
    Latest_low_price = float(Latest_low_price)

    if Latest_closing_price <= 20/100 * Latest_low_price:
        print("Buy")
        print("because the stock's latest closing price is exceeds threshold", "threshold:", Latest_closing_price)

    else:
        print("Don't Buy")
