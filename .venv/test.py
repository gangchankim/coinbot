import pyupbit
import logging
import bot
import threading
import requests
import time

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)


def getAllMarket():
    url = "https://api.upbit.com/v1/market/all?isDetails=false"
    headers = {"accept": "application/json"}
    try:
        res = requests.get(url, headers=headers)
        # print(res.text)
        return res.json()
    except:
        return None


# getAllMarket()


def getTickers(markets):
    headers = {"accept": "application/json"}
    try:
        res = requests.get(
            f"https://api.upbit.com/v1/ticker?markets={markets}", headers=headers)
        # print(res.text)
        return res.json()
    except:
        return None

# getTickers("KRW-BTC")


class UpbitThread(threading.Thread):
    def __init__(self):
        super(UpbitThread, self).__init__()
        self.daemon = True
        # 심볼이랑 시세 담기
        markets = getAllMarket()
        markets1 = getAllMarket()

        krwMarkets = list(
            filter(lambda market: market["market"].startswith(
                "KRW-"), markets)
        )
        self.markets = list(map(lambda market: market["market"], krwMarkets))
        self.symbols = ",".join(self.markets)
        self.data = []

        # KRW심볼 + 한국어 코인이름 담기
        self.markets1 = list(
            map(
                lambda x: [x["market"], x["korean_name"]],
                filter(
                    lambda x: 'market' in x and x["market"].startswith(
                        "KRW-") and 'korean_name' in x,
                    markets1
                )
            )
        )
        self.data1 = []

    def run(self):
        while True:
            # Getting the upbit market datas
            self.data = getTickers(self.symbols)
            self.data1 = self.markets1
            time.sleep(5)


upbitThread = UpbitThread()
upbitThread.start()

# 종목 이름과 시세 출력하기
while True:
    for ticker in upbitThread.data:
        market = ticker['market']
        coin_name = next(
            (m[1] for m in upbitThread.markets1 if m[0] == market), None)
        if coin_name:
            trade_price = ticker['trade_price']
            print(f"{coin_name}, {trade_price}")
    time.sleep(2)
