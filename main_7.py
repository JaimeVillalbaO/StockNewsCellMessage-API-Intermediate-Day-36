
## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 

## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 

import requests
from twilio.rest import Client
from datetime import datetime, timedelta
import os

STOCK = "TSLA"
news_api_password = os.environ.get('NEWS_API_PASSWORD')
stock_api_password = os.environ.get('STOCK_API_PASSWORD')


url_stock_price = ('https://www.alphavantage.co/query?'
                'function=TIME_SERIES_DAILY&'
                'symbol=TSLA&'
                f'apikey={stock_api_password}')

response_stock = requests.get(url_stock_price)
data = response_stock.json()["Time Series (Daily)"]
data_list = [v for k, v in data.items()]
day_before_yesterday_close_data = data_list[1]['4. close']
yesterday_close_data = data_list[0]['4. close']
# print(day_before_yesterday_close_data)
# print(yesterday_close_data)

difference = float(day_before_yesterday_close_data)-float(yesterday_close_data)
porcentage = round(abs(difference)*100/float(day_before_yesterday_close_data) )
print(porcentage)

if difference > 0:
    symbol = '🔺'
else:
    symbol = '🔻'




today_date = datetime.now()
today_formatted = today_date.strftime("%Y-%m-%d")

yesterday_date = today_date - timedelta(days=1)
yesterday_formatted = yesterday_date.strftime("%Y-%m-%d")


url_news = ('https://newsapi.org/v2/everything?'
       'q=Tesla&'
       f'from={yesterday_formatted}&'
       f'to={today_formatted}&'
       'lenguaje=en'
       'sortBy=popularity&'
       f'apiKey={news_api_password}')

response_news = requests.get(url_news)
tittle = response_news.json() ['articles'][0]['title']
# print(tittle)
description = response_news.json()['articles'][0]['description']
# print(tittle)
# print(description)

account_sid = os.environ.get('ACCOUNT_ID')
auth_token = os.environ.get('AUTH_TOK')

if porcentage >= 1:
    client = Client(account_sid, auth_token)
    message = client.messages\
        .create(
        body=f'{STOCK} {symbol} {porcentage}%\n'
            f'Headline: {tittle}\n'
            f'Brief: {description}',
        from_='+16592765022',
        to='+573215696357',
    )
    print(message.status)