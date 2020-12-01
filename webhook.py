from config import *
import requests


def telegram_init():
    requests.get(TELEGRAM_INIT_WEBHOOK_URL)



telegram_init()