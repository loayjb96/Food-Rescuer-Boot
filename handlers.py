from buttons import *
from message import send_post_message, send_get_message
from receiver import Reciver
from location import Location
from donator import Donator
from datetime import datetime, timedelta,date




#this needs to be removed
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

    
#--------------------------


#---- donator or reciever


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
    #needs replacing
    elif answer == 'Donator':
        print("were in donator")
        if id not in id_obj_map:
            print("id was not found creating new")
            rec = Donator()
            
            rec.set_id(message.get_id())
            id_obj_map[message.get_id()] = rec
    print("in handle type answer   :"+answer)
    handle_location(message, request, id_obj_map)


#----- location

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

    #continuing with the donation flow
    if type(id_obj_map[message.get_id()]) == Donator:
        #print("should continue to experation day")
        handle_experation_day(message, request, id_obj_map)


#---- experation date
experation_day_options =['Today only', '2 days', '3 days', 'frozen']
experation_day_options_values = [0,1,2,30]
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

    #todo : remove this 
    # print(id_obj_map[id])
    # print(id_obj_map[id].m_food_being_built)
    # id_obj_map[id].m_food_being_built.set_experation_day_in_x_days(5)
    # print(id_obj_map[id].m_food_being_built.m_expiration_date)
    # print(id_obj_map[id].m_food_being_built)

    i = 0
    for option in experation_day_options:
        if option == answer:
            id_obj_map[id].m_food_being_built.set_experation_day_in_x_days(experation_day_options_values[i])
        i += 1

    # if answer == experation_day_options[0]:
    #     print("today")
    #     id_obj_map[id].m_food_being_built.set_experation_day_in_x_days(0)

    # elif answer == experation_day_options[1]:
    #     print("today+1")
    #     id_obj_map[id].m_food_being_built.set_experation_day_in_x_days(1)
    # elif answer == experation_day_options[2]:
    #     print("today+2")
    #     id_obj_map[id].m_food_besing_built.set_experation_day_in_x_days(2)
    # elif answer == experation_day_options[3]:
    #     print("today+3")
    #     id_obj_map[id].m_food_being_built.set_experation_day_in_x_days(3) 
    print("days experation :" , id_obj_map[id].m_food_being_built.m_expiration_date)
    handle_num_of_servings(message, request, id_obj_map)


#---- serving size

serving_size_options = ['1', '2', '3', '4+']
serving_size_options_values = [1,2,3,4]

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

    print("you can add food to DB")
#----- add info
