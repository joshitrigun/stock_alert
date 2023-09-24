import requests
import os
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
STOCK_API_KEY = os.environ.get("OWN_STOCK_API_KEY")
NEWS_API_KEY = os.environ.get("OWN_NEWS_API_KEY")
TWILIO_SID = os.environ.get("OWN_TWILIO_SID")
TWILIO_AUTH_TOKEN = os.environ.get("OWN_TWILIO_AUTH_TOKEN")

STOCK_PARAMS = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY
}

NEWS_PARAMS = {
    "qInTitle": COMPANY_NAME,
    "apiKey": NEWS_API_KEY
}
# https://newsapi.org/v2/everything?q=tesla&from=2023-08-23&sortBy=publishedAt&apiKey=6b3cf6724e414ea58f349aeecfcbe1d9
## STEP 1: Use https://www.alphavantage.co/documentation/#daily
# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

# Get yesterday's closing stock price. Hint: You can perform list comprehensions on Python dictionaries. e.g. [new_value for (key, value) in dictionary.items()]

response = requests.get(STOCK_ENDPOINT, params=STOCK_PARAMS)
response.raise_for_status()
data = response.json()["Time Series (Daily)"]
# // list comprehension
data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
yesterday_close = yesterday_data["4. close"]

# print("yesterday_close", yesterday_close)



# Get the day before yesterday's closing stock price
day_before_yesterday_close = data_list[1]["4. close"]
# print('day_before_yesterday_close', day_before_yesterday_close)

# Find the positive difference between 1 and 2. e.g. 40 - 20 = -20, but the positive difference is 20. Hint: https://www.w3schools.com/python/ref_func_abs.asp
difference = abs(float(yesterday_close) - float(day_before_yesterday_close))
# print("difference", round(difference))

# Work out the percentage difference in price between closing price yesterday and closing price the day before yesterday.
diff_percent = (difference/float(yesterday_close)) * 100

# print("diff_percent", diff_percent)
#  If TODO4 percentage is greater than 5 then print("Get News").
if diff_percent > 4:
    # print("Get News")
    # Instead of printing ("Get News"), use the News API to get articles related to the COMPANY_NAME.
    res_news_api = requests.get(NEWS_ENDPOINT, params=NEWS_PARAMS)
    res_news_api.raise_for_status()
    articles = res_news_api.json()["articles"]
    #  Use Python slice operator to create a list that contains the first 3 articles. Hint: https://stackoverflow.com/questions/509211/understanding-slice-notation
    top_three_articles = articles[:3]
    # print(top_three_articles)

## STEP 3: Use twilio.com/docs/sms/quickstart/python
# to send a separate message with each article's title and description to your phone number.

# TODO 8. - Create a new list of the first 3 article's headline and description using list comprehension.
    formatted_articles = [f"Headline: {article['title']}. \n Brief: {article['description']}" for article in top_three_articles]
# TODO 9. - Send each article as a separate message via Twilio.
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    for a in formatted_articles:
        message = client.messages.create(
            body= a,
            from_= "+12184058212",
            to = "+12368676365"
        )

# Optional TODO: Format the message like this:
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""
