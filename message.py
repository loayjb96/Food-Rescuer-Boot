from config import MESSAGES_URL
import requests


class Message:
    def __init__(self, message):
        self.message = message
        self.action = None
        self.params = None
        self.id = None
        self.process_message()

    def process_message(self):
        self.id = self.message['chat']['id']
        splitted_msg = self.message['text'].split()

        if len(splitted_msg) != 2:
            self.action = None
            self.params = None
        else:
            self.action = splitted_msg[0]
            if splitted_msg[1].isnumeric():
                self.params = int(splitted_msg[1])

    def get_action(self):
        return self.action

    def get_params(self):
        return self.params

    def get_id(self):
        return self.id


def send_message(chat_id, message):
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
