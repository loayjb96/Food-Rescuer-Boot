from config import MESSAGES_URL
import requests


class Message:
    def __init__(self, message):
        self.message = message
        self.action = None
        self.id = None
        self.process_message()

    def process_message(self):
        self.id = self.message['chat']['id']
        self.action = self.message['text']

    def get_action(self):
        return self.action

    def get_id(self):
        return self.id


def send_get_message(chat_id, message):
    try:
        url = f"{MESSAGES_URL}?chat_id={chat_id}&text={message}"
        requests.get(url)
    except Exception as e:
        print("Error -", e)


def send_post_message(chat_id, message, data):
    try:
        url = f"{MESSAGES_URL}?chat_id={chat_id}&text={message}"
        requests.post(url, data=data)
    except Exception as e:
        print("Error -", e)
