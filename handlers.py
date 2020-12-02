from buttons import *
from message import send_post_message, send_get_message
from receiver import Reciver
from location import Location
from donator import Donator
from datetime import datetime, timedelta, date
from database import main_db, get_max_id
# --------------------------

# ---- donator or reciever


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
    elif answer == 'Donator':
        print("were in donator")
        if id not in id_obj_map:
            print("id was not found creating new")
            rec = Donator()
            rec.set_id(message.get_id())
            id_obj_map[message.get_id()] = rec
    print("in handle type answer   :" + answer)
    handle_location(message, request, id_obj_map)


# ----- location

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

    if type(id_obj_map[message.get_id()]) == Donator:
        handle_food_types(message, id_obj_map)
    elif type(id_obj_map[message.get_id()]) == Reciver:
        handle_receiver_food_types(message, id_obj_map)




#-----------------handle food  typr for donator

def handle_food_types(message, id_obj_map):
    food_type_options = ['Halal', 'Kosher', 'Vegetarian', 'Vegan', 'Animals', 'Other', 'Done']
    print("HANDLE FOOD type for a specific meal")
    DonatorId = message.get_id()
    currentMeal = id_obj_map[DonatorId].m_food_being_built


   
    signs_list = []
    # print(signs_list)
    # print("1")
    # signs_list.append('✔')
    # print(signs_list)
    # print("2")
    # signs_list.append('-')
    # print(signs_list)
    # print("3")
    for food_type in food_type_options:
        print(signs_list)
        if food_type in currentMeal.m_food_types:
            signs_list.append('✔')
        else:
            signs_list.append('-')

    sign_list_2 = [( '✔' if (food_type in currentMeal.m_food_types) else  '-') for food_type in food_type_options]

        
    print("after adding")

    print(sign_list_2)
    print("created buttons")
    servings_options = get_poll_buttons(food_type_options,  ['✔'] * 7)  #sign_list_2)
    print("created buttons")
    data = {
        "chat_id": message.get_id(),
        "reply_markup": servings_options
    }
    send_post_message(data.get('chat_id'), 'added to meal type', data)


def handle_food_types_response(message, request, id_obj_map):
    answer = request['callback_query']['data']
    id = message.get_id()
    if answer == 'Done':
        #add_recevier_to_db(id_obj_map[id])  todo: add adding food to DB
        handle_experation_day(message, request, id_obj_map)
        return
    id_obj_map[id].m_food_being_built.add_food_type(answer)
    send_get_message(id, f"{answer} added !")


# ---- experation date
experation_day_options = ['Today only', '2 days', '3 days', 'frozen']
experation_day_options_values = [0, 1, 2, 30]


def handle_experation_day(message, request, id_obj_map):
    servings_options = get_inline_buttons(experation_day_options)
    data = {
        "chat_id": message.get_id(),
        "reply_markup": servings_options
    }
    send_post_message(data.get('chat_id'), 'The food is good for?', data)


def handle_experation_day_response(message, request, id_obj_map):
    answer = request['callback_query']['data']
    id = message.get_id()

    i = 0
    for option in experation_day_options:
        if option == answer:
            id_obj_map[id].m_food_being_built.set_experation_day_in_x_days(experation_day_options_values[i])
        i += 1

    print("days experation :", id_obj_map[id].m_food_being_built.m_expiration_date)
    handle_num_of_servings(message, request, id_obj_map)


# ---- serving size

serving_size_options = ['1', '2', '3', '4+']
serving_size_options_values = [1, 2, 3, 4]


def handle_num_of_servings(message, request, id_obj_map):
    print("we are in number of servings")
    servings_options = get_inline_buttons(serving_size_options)
    data = {
        "chat_id": message.get_id(),
        "reply_markup": servings_options
    }
    send_post_message(data.get('chat_id'), 'How many people is the meal for?', data)


def handle_num_of_servings_response(message, request, id_obj_map):
    print("were in number of servings response")
    answer = request['callback_query']['data']
    id = message.get_id()

    i = 0
    for option in serving_size_options:
        if option == answer:
            id_obj_map[id].m_food_being_built.set_number_of_servings(serving_size_options_values[i])
        i += 1
    add_donator_to_db(id_obj_map[id])

#----------- handle food for client
def handle_receiver_food_types(message, id_obj_map):
    print("HANDLE FOOD  for reciever")
    servings_options = get_poll_buttons(['Halal', 'Kosher', 'Vegetarian', 'Vegan', 'Animals', 'Other', 'Done'],
                                        ['✔'] * 7)
    data = {
        "chat_id": message.get_id(),
        "reply_markup": servings_options
    }
    print("ended handling food for reciever")
    send_post_message(data.get('chat_id'), 'choose your food type', data)


def handle_receiver_food_types_response(message, request, id_obj_map):
    answer = request['callback_query']['data']
    id = message.get_id()
    if answer == 'Done':
        add_recevier_to_db(id_obj_map[id])
        
        return
    id_obj_map[id].add_receiver_food(answer)
    send_get_message(id, f"{answer} added to your food list!")


def add_donator_to_db(donator):
    print("ADD DONATOR")
    id = donator.m_id
    location = donator.m_location
    donation_count = donator.m_donation_counter
    donation_level = donator.m_donator_level
    location_to_db = {'id': '0',
                      'longitude': location.longitude,
                      'latitude': location.latitude
                      }
    main_db('add_location', location_to_db)

    donator_to_db = {
        'id': id,
        'user_name': 'null',
        'location_id': get_max_id('location'),
        'donation_count': donation_count,
        'donation_level': donation_level
    }
    main_db('add_donator', donator_to_db)
    food_to_db = {
        'id': '0',
        'donator_id': id,
        'location_id': donator_to_db['location_id'],
        'available': 1,
        'number_of_servings': donator.m_food_being_built.m_number_of_servings,
        'expiration_date': datetime.timestamp(donator.m_food_being_built.m_expiration_date),
        'description': donator.m_food_being_built.m_description,
        'food_types': donator.m_food_being_built.m_food_types
    }
    print("FOOD TO DB", food_to_db)
    main_db('add_food', food_to_db)
    send_get_message(id, f"You have added new MEAL!!")


def add_recevier_to_db(receiver):
    id = receiver.telegram_id
    location = receiver.location
    food_types = receiver.food_types
    location_to_db = {'id': '0',
                      'longitude': location.longitude,
                      'latitude': location.latitude
                      }
    main_db('add_location', location_to_db)
    receiver_to_db = {'id': id,
                      'location_id': get_max_id('location'),
                      'food_types': food_types}

    main_db('add_receiver', receiver_to_db)

    send_get_message(id, f"You have been added to the DB!")
    print("enter db")
    print()



    