import logging
import os

# создаём папку logs, если её нет
os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/bot.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def log_info(message: str):
    logging.info(message)


def log_error(message: str):
    logging.error(message)