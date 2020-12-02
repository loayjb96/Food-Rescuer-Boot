import json

from telegram import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, \
    KeyboardButtonPollType, poll, Poll


def get_keyboard_buttons(options):
    custom_keyboard = []
    for option in options:
        if option == 'Share My Location':
            custom_keyboard.append(KeyboardButton(text=option, request_location=True))
        else:
            custom_keyboard.append(KeyboardButton(text=option))
    custom_keyboard = [custom_keyboard]
    reply_markup = ReplyKeyboardMarkup(custom_keyboard, one_time_keyboard=True, resize_keyboard=True)
    return json.dumps(reply_markup.to_dict())


def get_inline_buttons(options):
    custom_keyboard = []
    for option in options:
        custom_keyboard.append(InlineKeyboardButton(text=option, callback_data=option))
    custom_keyboard = [custom_keyboard]
    reply_markup = InlineKeyboardMarkup(custom_keyboard)
    return json.dumps(reply_markup.to_dict())


def get_poll_buttons(options, selected):
    markup = []
    options_keyboard = []
    selected_keyboard = []

    for value1, value2 in zip(options, selected):
        options_keyboard.append([InlineKeyboardButton(text=value1,callback_data=value1),
                                InlineKeyboardButton(text=value2,callback_data=value2)] )

        reply_markup = InlineKeyboardMarkup(options_keyboard, one_time_keyboard=True)
    return json.dumps(reply_markup.to_dict())
