request_url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol="+symbol+"&apikey="+api_key # this is the url
response = requests.get(request_url) #this is a json
response_body = json.loads(response.text) #this is a list of dictionaries
last_refreshed = response_body["Meta Data"]["3. Last Refreshed"] #this takes the last refreshed data
data = response_body["Time Series (Daily)"] # this is still a dictionary. A dictionary of the time series (daily)
keys = data.keys()
all_dates = list(keys) # a list of the (dates)
symbol2 = symbol.upper() #this makes all the dates uppercase
today = dates[0] #this is the latest date
latest_price_usd = data[today]["4. close"] # this takes the closing price of the latest date.
print("Closing price on "+today+ "for "+symbol2 +" is: "+"(${0:.2f})".format(float(latest_price_usd)))
high_prices = [] #this starts the list of "high" prices
for d in dates: #this loops through the dates, and appends the high prices for each dates into the list.
    high_prices.append(data[d]["2. high"])
average_high_price = max(high_prices) #this sets average_high_price to the maximum high price
#you can do the same for low prices using min()
