import requests
import os
from twilio.rest import Client

twilio_account_sid = os.environ.get("TWILIO_SID")
twilio_auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
from_phone = os.environ.get("FROM_PHONE")
to_phone = os.environ.get("TO_PHONE")

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": os.environ.get("ALPHA_API_KEY"),
}
res = requests.get(STOCK_ENDPOINT, params=params)
data = res.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]
current = float(data_list[0]["4. close"])
previous = float(data_list[1]["4. close"])
diff = abs(current - previous)
percent = (diff / current) * 100
direction = ""

if current > previous:
    direction = "🔺"
else:
    direction = "🔻"

if percent > 1.5:
    news_params = {
        "qInTitle": COMPANY_NAME,
        "apiKey": os.environ.get("NEWS_API_KEY")
    }
    res = requests.get(NEWS_ENDPOINT, news_params)
    articles = res.json()["articles"]
    top_3 = articles[:3]

    news_list = [f"{STOCK_NAME} {direction} {round(percent, 1)}% \nHeadline: {article['title']}. \nBrief: {article['description']}" for article in top_3]

    client = Client(twilio_account_sid, twilio_auth_token)

    for msg in news_list:
        message = client.messages.create(
            body=msg,
            from_=from_phone,
            to=to_phone,
        )

        print(message.status)


