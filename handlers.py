import json

from telegram import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

def handle_choosing_user_type():
    return "HEY"


def get_location(number):
    print("start")
    location_keyboard = KeyboardButton(text="Share My Location", request_location=True)
    contact_keyboard = KeyboardButton(text="Share My Contact", request_contact=True)
    custom_keyboard = [[location_keyboard, contact_keyboard]]
    reply_markup = ReplyKeyboardMarkup(custom_keyboard, one_time_keyboard=True, resize_keyboard=True)
    print("end\n")
    print(json.dumps(reply_markup.to_dict()))
    return json.dumps(reply_markup.to_dict())
