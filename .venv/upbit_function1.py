import pyupbit
import logging
import bot

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

# 잔고 불러오기


async def get_balance(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    res = bot.client.get_balances()

    if "error" in res:
        await update.message.reply_text(
            f"불러오기 실패(이유: {res['error']['message']})",
        )
    else:
        # KRW 인 것은 제외하고, avg_buy_price 값이 없으면 에어드랍 코인으로 간주
        filteredBalance = list(
            filter(
                lambda d: d["currency"] == "KRW"
                or (d["avg_buy_price"] != "0"
                    and d["currency"] != "FUN"
                    and d["currency"] != "OK"
                    and d["currency"] != "USDT"
                    ),
                res,
            )
        )

        message = "[잔고 목록]\n\n티커   개수\n"

        for balance in filteredBalance:
            message += f"{balance['currency']}   {balance['balance']}\n"

        await update.message.reply_text(message)

# 주문중인 잔고 불러오기


async def get_ordered(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    res = bot.client.get_balances()

    if "error" in res:
        await update.message.reply_text(
            f"불러오기 실패(이유: {res['error']['message']})",
        )
    else:
        # KRW 인 것은 제외하고, avg_buy_price 값이 없으면 에어드랍 코인으로 간주
        filteredBalance = list(
            filter(
                lambda d: d["currency"] == "KRW"
                or (d["avg_buy_price"] != "0"
                    and d["currency"] != "FUN"
                    and d["currency"] != "OK"
                    and d["currency"] != "USDT"
                    ),
                res,
            )
        )

        message = "[잔고 목록]\n\n티커   개수\n"

        for balance in filteredBalance:
            message += f"{balance['currency']}   {balance['locked']}\n"

        await update.message.reply_text(message)
