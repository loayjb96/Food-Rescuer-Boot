from buttons import *
from message import send_post_message, send_get_message
from receiver import Reciver
from location import Location
from donator import Donator
from datetime import datetime, timedelta, date
from database import main_db, get_max_id
from box import box

# this needs to be removed
donators = []


def get_donator_by_id(donator_id):
    for don in donators:
        if don.m_id == donator_id:
            return don
    return None


def add_donator_if_doesnt_exist(donator_id):
    if get_donator_by_id(donator_id) == None:
        donator_to_add = Donator()
        donator_to_add.m_id = donator_id
        donators.append(Donator)
        return get_donator_by_id(donator_id)


# ---- donator or reciever


def handle_choosing_user_type(message, request, id_obj_map):
    user_types = get_inline_buttons(['Donator', 'Receiver'])
    data = {
        "chat_id": message.get_id(),
        "reply_markup": user_types
    }
    send_post_message(data.get('chat_id'), 'Are you a Donator or Receiver?', data)


def get_receiver_by_id(id):
    rec = main_db('get_receiver_by_id', id)
    if not rec:
        return None
    else:
        new_rec = Reciver()
        new_rec.init_reciver_id(id)
        location = main_db('get_location_by_id', rec['location_id'])
        new_location = Location()
        new_location.set_address(location['longitude'], location['latitude'])
        new_rec.set_location(new_location)
        new_rec.food_types = main_db('get_receiver_food_types_by_id', id)
    return new_rec


def handle_type_answer(message, request, id_obj_map):
    answer = request['callback_query']['data']
    id = message.get_id()

    if answer == 'Receiver':
        rec = get_receiver_by_id(id)
        if not rec:
            rec = Reciver()
            rec.init_reciver_id(id)
            id_obj_map[id] = rec
        else:
            id_obj_map[id] = rec
            handle_exciting_receiver_in_db(message, request, id_obj_map)
            return
    elif answer == 'Donator':
        rec = Donator()
        rec.set_id(message.get_id())
        id_obj_map[message.get_id()] = rec

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
    print("ENTERED LOCATION")
    location = Location()
    print("REQ", request)
    res_location = request.get('message').get('location')
    print("LOC", res_location)
    location.set_address(res_location['latitude'], res_location['longitude'])
    id_obj_map[message.get_id()].set_location(location)
    print("LOCATION", location)
    if type(id_obj_map[message.get_id()]) == Donator:
        handle_food_types(message, id_obj_map)
    elif type(id_obj_map[message.get_id()]) == Reciver:
        print("ENTERED RECEIVER")
        handle_receiver_food_types(message, id_obj_map)


# -----------------handle food  typr for donator

def handle_food_types(message, id_obj_map):
    food_type_options = ['Halal', 'Kosher', 'Vegetarian', 'Vegan', 'Animals', 'Other', 'Done']
    print("HANDLE FOOD type for a specific meal")
    DonatorId = message.get_id()
    currentMeal = id_obj_map[DonatorId].m_food_being_built
    sign_list_2 = [('✔' if (food_type in currentMeal.m_food_types) else '-') for food_type in food_type_options]

    print("after adding")

    print(sign_list_2)
    print("created buttons")
    servings_options = get_poll_buttons(food_type_options, sign_list_2)
    print("created buttons")
    data = {
        "chat_id": message.get_id(),
        "reply_markup": servings_options
    }
    send_post_message(data.get('chat_id'), 'added to meal type', data)


def handle_food_types_response(message, request, id_obj_map):
    answer = request['callback_query']['data']
    id = message.get_id()
    print(answer + " was selected")
    if answer == 'Done':
        # add_recevier_to_db(id_obj_map[id])  todo: add adding food to DB
        print("done selection")
        handle_experation_day(message, request, id_obj_map)
        return

    if answer != '✔' and answer != '-':
        print("not signs")
        if answer in id_obj_map[id].m_food_being_built.m_food_types:
            print("already added")
            id_obj_map[id].m_food_being_built.remove_food_type(answer)
            send_get_message(id, f"{answer} removed !")
        else:
            print("not added before")
            id_obj_map[id].m_food_being_built.add_food_type(answer)
            send_get_message(id, f"{answer} added !")
        handle_food_types(message, id_obj_map)


# ---- experation date
experation_day_options = ['Today only', '2 days', '3 days', 'frozen']
experation_day_options_values = [0, 1, 2, 30]


def handle_experation_day(message, request, id_obj_map):
    print("in experation day")
    servings_options = get_inline_buttons(experation_day_options)
    print("created buttons")
    data = {
        "chat_id": message.get_id(),
        "reply_markup": servings_options
    }
    print("going to send")

    send_post_message(data.get('chat_id'), 'The food is good for?', data)
    print("sent")


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


# ----------- handle food for client
def handle_receiver_food_types(message, id_obj_map):
    print("HANDLE FOOD  for reciever")
    food_type_options = ['Halal', 'Kosher', 'Vegetarian', 'Vegan', 'Animals', 'Other', 'Done']
    reciverId = message.get_id()

    sign_list_2 = [('✔' if (food_type in id_obj_map[reciverId].food_types) else '-') for food_type in food_type_options]

    
    servings_options = get_poll_buttons(food_type_options ,sign_list_2)
    data = {
        "chat_id": message.get_id(),
        "reply_markup": servings_options
    }
    print("ended handling food for reciever")
    send_post_message(data.get('chat_id'), 'choose your food type', data)


def handle_receiver_food_types_response(message, request, id_obj_map):
    answer = request['callback_query']['data']
    id = message.get_id()
    print(answer)
    if answer == 'Done':
        add_recevier_to_db(id_obj_map[id])
        handle_add_receiver_process_end(message)
        return

    if answer != '✔' and answer != '-':
        print("not signs")
        if answer in id_obj_map[id].m_food_being_built.m_food_types:
            print("already added")
            id_obj_map[id].remove_food_type(answer)
            send_get_message(id, f"{answer} removed !")
        else:
            print("not added before")
            id_obj_map[id].add_food_type(answer)
            send_get_message(id, f"{answer} added !")
        handle_food_types(message, id_obj_map)

    id_obj_map[id].add_receiver_food(answer)
    send_get_message(id, f"{answer} added to your food list!")
    handle_receiver_food_types(message, id_obj_map)


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


def handle_add_receiver_process_end(message):
    show_db = get_inline_buttons(['Show food', 'skip'])
    data = {
        "chat_id": message.get_id(),
        "reply_markup": show_db
    }
    send_post_message(data.get('chat_id'), 'Show food', data)


def handle_receiver_end_response(message, request, id_obj_map):
    answer = request['callback_query']['data']
    id = message.get_id()
    if answer == 'Show food':
        send_get_message(id, f"{answer} was pressed!")
        show_food_list(id, id_obj_map[id])
        return
    elif answer == 'skip':
        send_get_message(id, f"{answer} was pressed!")


# private func..
def get_relative_distance_for_receiver(receiver, food_list):
    ids_distance = {}
    for food in food_list:
        print("MY LOCATION", receiver.location, "FOOD LOCATION", food['location'])
        if food['id'] in ids_distance:
            ids_distance[food['id']] = min(ids_distance[food['id']],
                                           receiver.get_relative_distance(food['location']))
        else:
            ids_distance[food['id']] = receiver.get_relative_distance(food['location'])
    return dict(sorted(ids_distance.items(), key=lambda item: item[1]))


def show_food_list(chat_id, receiver):
    food_list = main_db('get_food_by_types', receiver.food_types)
    print("FOOD LIST", food_list, receiver)
    relative_distance = get_relative_distance_for_receiver(receiver, food_list)
    food_list = {food['id']: food for food in food_list}

    for id in relative_distance:
        item = food_list[id]
        number_of_servings = item['number_of_servings']
        food_types = ", ".join(item['food_types'])
        user_name = '@kar2357'
        location = round(relative_distance[id], 5)
        print(location)

        send_get_message(chat_id, box(id, number_of_servings, food_types, str(location), user_name))


def handle_exciting_receiver_in_db(message, request, id_obj_map):
    user_types = get_inline_buttons(['Show food', 'Edit Profile'])
    data = {
        "chat_id": message.get_id(),
        "reply_markup": user_types
    }
    send_post_message(data.get('chat_id'), 'what would you like to do?', data)


def handle_exciting_receiver_in_db_responce(message, request, id_obj_map):
    answer = request['callback_query']['data']
    id = message.get_id()
    if answer == 'Show food':
        send_get_message(id, f"{answer} was pressed!")
        print(id, id_obj_map)
        show_food_list(id, id_obj_map[id])
    elif answer == 'Edit Profile':
        main_db('delete_receiver_by_id', id)
        del id_obj_map[id]
        rec = Reciver()
        rec.init_reciver_id(id)
        id_obj_map[id] = rec
        handle_location(message, request, id_obj_map)
        # send_get_message(id, f"{answer} was pressed!")
