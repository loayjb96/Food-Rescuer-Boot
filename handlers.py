from buttons import *
from message import send_post_message, send_get_message
from receiver import Reciver
from location import Location
from donator import Donator
from datetime import datetime, timedelta, date
from database import main_db, get_max_id
from photo import *
import pathlib
from config import MESSAGES_URL, TOKEN

import telegram

from box import box, meal_box

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


def handle_choosing_user_type(message, request, id_obj_map):
    print("HERE")
    user_types = get_inline_buttons(['Donator', 'Receiver'])
    data = {
        "chat_id": message.get_id(),
        "reply_markup": user_types
    }
    send_post_message(data.get('chat_id'), 'Are you a Donator or Receiver? 🧐', data)


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
        print("MY LOCATION IN GET", new_location)
        new_rec.set_location(new_location)
        new_rec.food_types = main_db('get_receiver_food_types_by_id', id)
    return new_rec


def handle_type_answer(message, request, id_obj_map):
    answer = request['callback_query']['data']
    id = message.get_id()
    print("ENTERED HERE")
    if answer == 'Receiver':
        print("REC")
        rec = get_receiver_by_id(id)
        print("REC", rec)
        if not rec:
            rec = Reciver()
            rec.init_reciver_id(id)
            id_obj_map[id] = rec
            send_get_message(id, "💥💥 Welcome to Food Rescuer 💥💥\nWe hope we can be a helping hand 🙌🙏🤝")
        else:
            id_obj_map[id] = rec
            handle_exciting_receiver_in_db(message, request, id_obj_map)
            return
    elif answer == 'Donator':
        print("DONATOR")
        rec = Donator()
        # print("REQUEST", request)
        rec.user_name = request['callback_query']['from']['username']
        print(rec.user_name)
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
    # Please send your location
    send_post_message(data.get('chat_id'), 'Please send me your location 🗺', data)


def handle_location_response(message, request, id_obj_map):
    print("ENTERED LOCATION")
    location = Location()
    print("REQ", request)
    res_location = request.get('message').get('location')
    print("LOC", res_location)
    location.set_address(res_location['longitude'], res_location['latitude'])
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
    send_post_message(data.get('chat_id'), 'Ok, let me know more about your food preferences 🍗 🍕 🥗 ❓', data)


def handle_food_types_response(message, request, id_obj_map):
    answer = request['callback_query']['data']
    id = message.get_id()
    print(answer + " was selected")
    if answer == 'Done':
        print("done selection")
        handle_experation_day(message, request, id_obj_map)
        return
    iconse = {'Halal': '🍗', 'Kosher': '🍠', 'Vegetarian': '🥚', 'Vegan': '🥗', 'Animals': '🐕🐈', 'Other': '🌏🌐'}

    if answer != '✔' and answer != '-':
        print("not signs")
        if answer in id_obj_map[id].m_food_being_built.m_food_types:
            print("already added")
            id_obj_map[id].m_food_being_built.remove_food_type(answer)
            send_get_message(id, f"You removed {answer} {iconse.get(answer)} 😣")
        else:
            print("not added before")
            id_obj_map[id].m_food_being_built.add_food_type(answer)
            if answer == 'Animals':
                send_get_message(id, f"You chose {answer} {iconse.get(answer)} 🤩")
            elif answer == 'Other':
                send_get_message(id, f"You chose {answer} {iconse.get(answer)} 🤨")
            else:
                send_get_message(id, f"You chose {answer} {iconse.get(answer)} 🤤")
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
    #
    send_post_message(data.get('chat_id'), 'The food is good for? ⌚⌛', data)
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
    send_post_message(data.get('chat_id'), 'Ok, how many people is the meal for? 🤔', data)


def handle_num_of_servings_response(message, request, id_obj_map):
    print("were in number of servings response")
    answer = request['callback_query']['data']
    id = message.get_id()

    i = 0
    for option in serving_size_options:
        if option == answer:
            id_obj_map[id].m_food_being_built.set_number_of_servings(serving_size_options_values[i])
        i += 1
    add_donaitor_description(message, request, id_obj_map)


def add_donaitor_description(message, request, id_obj_map):
    id = message.get_id()
    send_get_message(id, "Please tell me more about the food by typing a small description 😛")


def handle_add_donaitor_description(message, request, id_obj_map):
    answer = request.get('message')['text']
    id = message.get_id()
    print(answer)
    id_obj_map[id].m_food_being_built.m_description = answer
    handle_add_photos(message, request, id_obj_map)


# ----------- handle food for client
def handle_receiver_food_types(message, id_obj_map):
    print("HANDLE FOOD  for reciever")
    food_type_options = ['Halal', 'Kosher', 'Vegetarian', 'Vegan', 'Animals', 'Other', 'Done']
    reciverId = message.get_id()

    sign_list_2 = [('✔' if (food_type in id_obj_map[reciverId].food_types) else '-') for food_type in food_type_options]

    servings_options = get_poll_buttons(food_type_options, sign_list_2)
    data = {
        "chat_id": message.get_id(),
        "reply_markup": servings_options
    }
    print("ended handling food for reciever")
    send_post_message(data.get('chat_id'), 'Ok, let me know more about your food preferences 🍗 🍕 🥗 ❓❔', data)


def handle_receiver_food_types_response(message, request, id_obj_map):
    answer = request['callback_query']['data']
    id = message.get_id()
    print(answer + " was selected")
    if answer == 'Done':
        add_recevier_to_db(id_obj_map[id])
        handle_add_receiver_process_end(message)
        return

    iconse = {'Halal': '🍗', 'Kosher': '🍠', 'Vegetarian': '🥚', 'Vegan': '🥗', 'Animals': '🐕🐈', 'Other': '🌏🌐'}
    if answer != '✔' and answer != '-':
        print("not signs")
        if answer in id_obj_map[id].food_types:
            print("already added")
            id_obj_map[id].remove_food_type(answer)
            send_get_message(id, f"You removed {answer} {iconse.get(answer)} 😣")
        else:
            print("not added before")
            id_obj_map[id].add_food_type(answer)
            if answer == 'Animals':
                send_get_message(id, f"You chose {answer} {iconse.get(answer)} 🤩")
            elif answer == 'Other':
                send_get_message(id, f"You chose {answer} {iconse.get(answer)} 🤨")
            else:
                send_get_message(id, f"You chose {answer} {iconse.get(answer)} 🤤")
        handle_receiver_food_types(message, id_obj_map)


def handle_add_photos(message, request, id_obj_map):
    print("PHOTOS")
    user_types = get_inline_buttons(['Add photos', 'Skip'])
    data = {
        "chat_id": message.get_id(),
        "reply_markup": user_types
    }
    # Do you want to add some photos?
    send_post_message(data.get('chat_id'), 'Do you want to add some photos⁉ 📷', data)


def handle_add_photos_response(message, request, id_obj_map):
    answer = request['callback_query']['data']
    id = message.get_id()
    if answer == 'Add photos':
        send_get_message(id, f"Yess‼ Please add as many photos as you want, but do not forget to type Done for me 🤗🤗")
    else:
        add_donator_to_db(id_obj_map[id])


def handle_add_photos_done(message, request, id_obj_map):
    print("DONE!")
    add_donator_to_db(id_obj_map[message.get_id()])


def add_donator_to_db(donator):
    print("ADD DONATOR")
    id = donator.m_id
    user_name = donator.user_name
    print("USER NAME", user_name)
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
        'user_name': user_name,
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
    if len(donator.photos) != 0:
        food_id = get_max_id('food')

        for photo_id in donator.photos:
            dir_path = f"Food{food_id}-"
            photo_path = save_photo_by_path(photo_id, dir_path)
            print("PATH", photo_path)
            main_db('add_photo', {'id': '0', 'path': photo_path})
            photo_db_id = get_max_id('photo')
            main_db('add_food_photos', {'id': '0', 'food_id': food_id, 'photo_id': photo_db_id})
        print("ID", food_id)

    send_get_message(id, meal_box("❤❤ Thank you for being part of reducing food waste ❤❤"))


def add_recevier_to_db(receiver):
    id = receiver.telegram_id
    location = receiver.location
    food_types = receiver.food_types
    print("FOOD TYPES", food_types)
    location_to_db = {'id': '0',
                      'longitude': location.longitude,
                      'latitude': location.latitude
                      }

    main_db('add_location', location_to_db)

    main_db('add_location', location_to_db)

    receiver_to_db = {'id': id,
                      'location_id': get_max_id('location'),
                      'food_types': food_types}

    main_db('add_receiver', receiver_to_db)


def handle_add_receiver_process_end(message):
    show_db = get_inline_buttons(['Show food', 'skip'])
    data = {
        "chat_id": message.get_id(),
        "reply_markup": show_db
    }

    send_post_message(data.get('chat_id'),
                      "Thank you for your cooperation 😍, I have saved all your information 😉\nWhat's next❓", data)


def handle_receiver_end_response(message, request, id_obj_map):
    answer = request['callback_query']['data']
    id = message.get_id()
    if answer == 'Show food':
        send_get_message(message.get_id(),
                         "Here is your relevant food with their contacts 🤗\nFeel free to contact the most appropriate one 😎")
        show_food_list(id, id_obj_map[id])
        return
    elif answer == 'skip':
        send_get_message(id, f"Ok, see you next time ❗👋👋")


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

        photos = main_db('get_photos_by_food_id',item.get('food_id'))

        donator = main_db('get_donator_by_id', item['donator_id'])
        number_of_servings = item['number_of_servings']
        food_types = ", ".join(item['food_types'])
        user_name = '@' + donator['user_name']
        location = round(relative_distance[id], 5)
        des = item['description']


        send_get_message(chat_id, box(id, number_of_servings, food_types, str(location), user_name, des))
        # for photo in photos:
        files = open('earth.jpg', 'rb')
        # send_post_message(chat_id,'',files)


        if len(photos) > 0:
            send_get_message(chat_id, box(id, number_of_servings, food_types, str(location), user_name, des,
                                          '\nPhotos of the meal:\n'))
            bot = telegram.Bot(token=TOKEN)
            for photo in photos:
                bot.send_photo(chat_id, open(photo, 'rb'))
        else:
            send_get_message(chat_id, box(id, number_of_servings, food_types, str(location), user_name, des))



def handle_exciting_receiver_in_db(message, request, id_obj_map):
    user_types = get_inline_buttons(['Show food', 'Restart Process'])
    data = {
        "chat_id": message.get_id(),
        "reply_markup": user_types
    }
    # what would you like to do?
    send_post_message(data.get('chat_id'), 'Ok, I see that you have been here before 😚\nWhat would you like to do?',
                      data)


def handle_exciting_receiver_in_db_responce(message, request, id_obj_map):
    answer = request['callback_query']['data']
    id = message.get_id()
    if answer == 'Show food':
        send_get_message(id,
                         f"Here is your relevant food with their contacts 🤗\nFeel free to contact the most appropriate one 😎")
        print(id, id_obj_map)
        show_food_list(id, id_obj_map[id])
    elif answer == 'Restart Process':
        main_db('delete_receiver_by_id', id)
        del id_obj_map[id]
        rec = Reciver()
        rec.init_reciver_id(id)
        id_obj_map[id] = rec
        handle_location(message, request, id_obj_map)
        # send_get_message(id, f"{answer} was pressed!")


def handle_photo_response(message, request, id_obj_map):
    photo = request['message']['photo']
    id = message.get_id()
    id_obj_map[id].photos.add(photo[-1]['file_id'])
    print("PHOTOS", id_obj_map[id].photos)
