import json

from telegram import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from buttons import *
from message import send_post_message


def handle_choosing_user_type(message, request):
    user_types = get_inline_buttons(['Donator', 'Receiver'])
    print(user_types)
    data = {
        "chat_id": message.get_id(),
        "reply_markup": user_types
    }
    send_post_message(data.get('chat_id'), 'Are you a Donator or Receiver?', data)


def handle_type_answer(message, request):
    print(message, request)


def handle_location(message, request):
    print("REQ", request)
    location_button = get_keyboard_buttons(['Share My Location'])
    data = {
        "chat_id": message.get_id(),
        "reply_markup": location_button
    }
    send_post_message(data.get('chat_id'), 'Please send your location', data)
