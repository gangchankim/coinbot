#!/usr/bin/env python
# pylint: disable=unused-argument, wrong-import-position
import pyupbit
import logging
import upbit_function1

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# 업비트 API 발급 받은 값을 넣어주세요.
access_key = ""
secret_key = ""

client = pyupbit.Upbit(access_key, secret_key)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        f"HELLO {user.mention_html()}님?",
    )


def main() -> None:
    """Run the bot."""
    # API 키 받은 것을 TOKEN 대신에 넣어준다.
    application = Application.builder().token(
        "6008825654:AAEXowN7Gr6W9b1UN7rA-hFIpoKvGfeyatw").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler(
        "balance", upbit_function1.get_balance))
    application.add_handler(CommandHandler(
        "locked", upbit_function1.get_ordered))
    application.run_polling()


if __name__ == "__main__":
    main()
