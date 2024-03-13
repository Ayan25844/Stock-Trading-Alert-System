
import requests,os
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

auth_token = os.environ.get("AUTH_TOKEN")
account_sid = os.environ.get("ACCOUNT_SID")

NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
STOCK_ENDPOINT = "https://www.alphavantage.co/query"

stock_params={
    "symbol":STOCK_NAME,
    "apikey":os.environ.get("STOCK_API_KEY"),
    "function":"TIME_SERIES_DAILY"
}

news_params={
    "qInTitle":COMPANY_NAME,
    "apikey":os.environ.get("NEWS_API_KEY")
}

stock_data=requests.get(url=STOCK_ENDPOINT,params=stock_params)

stock_data.raise_for_status()
closing_price_list=[value["4. close"] for (_,value) in stock_data.json()["Time Series (Daily)"].items()]

yesterday_closing_price=float(closing_price_list[0])
day_before_yesterday_closing_price=float(closing_price_list[1])
closing_price_percent_diff=abs(round(((yesterday_closing_price-day_before_yesterday_closing_price)/yesterday_closing_price)*100))

if(closing_price_percent_diff<5):

    news_data=requests.get(url=NEWS_ENDPOINT,params=news_params)
    news_data.raise_for_status()

    news_list=[f"{STOCK_NAME}: 🔺{closing_price_percent_diff}%\nHeadline: {article['title']}\nBrief: {article['description']}" for article in news_data.json()["articles"][:3]]

    client = Client(account_sid, auth_token)

    for text in news_list: 
        message = client.messages.create(
            body=text,
            from_='+15169793103',
            to='+911234567890'
        )
