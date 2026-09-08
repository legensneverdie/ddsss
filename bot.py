import os
import time
import logging
import requests
from telegram import Bot
from telegram.error import TelegramError

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
log = logging.getLogger("ton-price-bot")

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")  # e.g. @tonprices or -1001234567890
INTERVAL_SECONDS = int(os.getenv("INTERVAL_SECONDS", "60"))

COINGECKO_URL = "https://api.coingecko.com/api/v3/simple/price"
COINGECKO_PARAMS = {"ids": "the-open-network", "vs_currencies": "usd"}

if not BOT_TOKEN or not CHANNEL_ID:
    raise SystemExit("BOT_TOKEN и CHANNEL_ID должны быть заданы в переменных окружения")

bot = Bot(token=BOT_TOKEN)


def get_ton_price() -> float:
    resp = requests.get(COINGECKO_URL, params=COINGECKO_PARAMS, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    return data["the-open-network"]["usd"]


def post_price(price: float):
    text = f"{price:.2f}$"
    try:
        bot.send_message(chat_id=CHANNEL_ID, text=text)
        log.info(f"Posted: {text}")
    except TelegramError as e:
        log.error(f"Failed to send message: {e}")


def main():
    log.info("TON price bot started")
    while True:
        try:
            price = get_ton_price()
            post_price(price)
        except Exception as e:
            log.error(f"Error fetching/posting price: {e}")
        time.sleep(INTERVAL_SECONDS)


if __name__ == "__main__":
    main()
