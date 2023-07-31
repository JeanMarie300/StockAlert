import requests
from twilio.rest import Client
import os

STOCK = "SOFI"
COMPANY_NAME = "SOFI"

STOCK_API_KEY = os.getenv('STOCK_API_KEY')
NEWS_API_KEY = os.getenv('NEWS_API_KEY')

StockAPIParameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": STOCK_API_KEY
}


STOCK_API_EndPoint = "https://www.alphavantage.co/query"
NEWS_API_EndPoint = "https://newsapi.org/v2/everything"

#Twilio parameters
ACCOUNT_SID = os.getenv('ACCOUNT_SID')
AUTH_TOKEN = os.getenv('AUTH_TOKEN')

timestamps = []

percent_change = 0

StockResponse = requests.get(url=STOCK_API_EndPoint, params=StockAPIParameters)

daily_data = StockResponse.json()['Time Series (Daily)']

first_three_day_data = {k: daily_data[k] for k in list(daily_data)[:3]}
first_three_day_data_dict = dict(first_three_day_data)

for key, value in first_three_day_data_dict.items():
        timestamps.append(key)

yesterday_data = first_three_day_data_dict[timestamps[1]]
before_yesterday_data = first_three_day_data_dict[timestamps[2]]

yesterday_close_price = yesterday_data['4. close']
before_yesterday_close_price = before_yesterday_data['4. close']

percent_change = (float(yesterday_close_price) - float(before_yesterday_close_price)) / float(before_yesterday_close_price) * 100

if percent_change < 0 :
    arrow = "🔻"
else:
    arrow = "🔺"
if abs(percent_change) > 4:
    NewsParameters = {
        "q": COMPANY_NAME,
        "from": timestamps[1],
        "to": timestamps[2],
        "sortBy": "popularity",
        "apikey": NEWS_API_KEY
    }

    NewsResponses = requests.get(url=NEWS_API_EndPoint, params=NewsParameters)
    articles = NewsResponses.json()['articles'][:3]

    nameValue = f'{STOCK} :  {arrow} 4%'
    messageContent = f"{nameValue}"
    for article in articles :
        messageContent = messageContent + f"\n \n Headline : {article['title']} \n \n Brief : {article['description']}"

    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    message = client.messages.create(
    to=os.getenv('TO_PHONE_NUMBER'),
    from_=os.getenv('FROM_PHONE_NUMBER'),
    body=messageContent
)