from message import *
import handlers


class Bot:
    def __init__(self):
        self.handlers = {}
        self.id_obj_map = {}

    def add_handler(self, action, func):
        self.handlers[action] = func

    def action(self, request):
        try:
            if 'message' in request:
                message = request.get('message')
                if 'location' in message:
                    curr_msg = Message({'text': 'location response', 'chat': request.get('message').get('chat')})
                elif 'photo' in message:
                    curr_msg = Message({'text': 'add photo response', 'chat': request.get('message').get('chat')})
                elif message.get('text') != 'Done' and message.get('text') != '/start':
                    curr_msg = Message(request.get('message'))
                    handlers.handle_add_donaitor_description(curr_msg, request, self.id_obj_map)
                else:
                    curr_msg = Message(request.get('message'))
            else:
                message = {'text': request.get('callback_query').get('message').get('text'),
                           'chat': request.get('callback_query').get('message').get('chat')}
                curr_msg = Message(message)
            action = curr_msg.get_action()
            print("ACTION", action)
            self.handlers.get(action)(curr_msg, request, self.id_obj_map)

        except Exception as e:

            pass


def get_bot():
    bot = Bot()

    bot.add_handler('/start', handlers.handle_choosing_user_type)
    bot.add_handler('/location', handlers.handle_location)
    bot.add_handler('Are you a Donator or Receiver? 🧐', handlers.handle_type_answer)
    bot.add_handler('location response', handlers.handle_location_response)

    # bot.add_handler('Please send your location', handlers.handle_location_response)
    bot.add_handler('The food is good for? ⌚⌛', handlers.handle_experation_day_response)
    bot.add_handler('Ok, how many people is the meal for? 🤔', handlers.handle_num_of_servings_response)

    bot.add_handler('Ok, let me know more about your food preferences 🍗 🍕 🥗 ❓❔',
                    handlers.handle_receiver_food_types_response)
    bot.add_handler('Ok, let me know more about your food preferences 🍗 🍕 🥗 ❓', handlers.handle_food_types_response)

    bot.add_handler("Thank you for your cooperation 😍, I have saved all your information 😉\nWhat's next❓",
                    handlers.handle_receiver_end_response)
    bot.add_handler('Ok, I see that you have been here before 😚\nWhat would you like to do?',
                    handlers.handle_exciting_receiver_in_db_responce)

    bot.add_handler('Do you want to add some photos⁉ 📷', handlers.handle_add_photos_response)
    bot.add_handler('add photo response', handlers.handle_photo_response)
    bot.add_handler('Done', handlers.handle_add_photos_done)

    # bot.add_handler('You have added new MEAL!!', handlers.handle_exciting_receiver_in_db_responce)
    # bot.add_handler('Please tell me more about the food by writing small description 😛', handlers.handle_add_donaitor_description)

    return bot
