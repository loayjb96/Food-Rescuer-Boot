from buttons import *
from message import send_post_message, send_get_message
from receiver import Reciver
from location import Location
import donator

#this needs to be removed
donators = []

def add_donator_if_doesnt_exist(donator_id):
    donator_to_add = donator()
    donator_to_add
#


def handle_choosing_user_type(message, request, id_obj_map):
    user_types = get_inline_buttons(['Donator', 'Receiver'])
    data = {
        "chat_id": message.get_id(),
        "reply_markup": user_types
    }
    send_post_message(data.get('chat_id'), 'Are you a Donator or Receiver?', data)


def handle_type_answer(message, request, id_obj_map):
    answer = request['callback_query']['data']
    id = message.get_id()
    if answer == 'Receiver':
        if id not in id_obj_map:
            rec = Reciver()
            rec.init_reciver_id(message.get_id())
            id_obj_map[message.get_id()] = rec
    # TODO: add donator code
    handle_location(message, request, id_obj_map)


def handle_location(message, request, id_obj_map):
    location_button = get_keyboard_buttons(['Share My Location'])
    data = {
        "chat_id": message.get_id(),
        "reply_markup": location_button
    }
    send_post_message(data.get('chat_id'), 'Please send your location', data)


def handle_location_response(message, request, id_obj_map):
    location = Location()
    res_location = request.get('message').get('location')
    location.set_address(res_location['latitude'], res_location['longitude'])
    id_obj_map[message.get_id()].set_location(location)
    if type(id_obj_map[message.get_id()]) == Reciver:
        handle_num_of_servings(message, request, id_obj_map)


def handle_num_of_servings(message, request, id_obj_map):
    servings_options = get_inline_buttons(['1', '2', '3', '4'])
    data = {
        "chat_id": message.get_id(),
        "reply_markup": servings_options
    }
    send_post_message(data.get('chat_id'), 'How many servings the meal?', data)


def handle_num_of_servings_response(message, request, id_obj_map):
    print("ENTERED")
    answer = request['callback_query']['data']
    id = message.get_id()
    send_get_message(id, f"Your answer is {answer}")


