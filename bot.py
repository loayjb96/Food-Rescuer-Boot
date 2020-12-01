from message import *
import handlers


class Bot:
    def __init__(self):
        self.flow_graph = {}
        self.handlers = {}
        self.receivers = []
        self.donators = []
        self.id_obj_map = {}
        self.build_flow()

    def build_flow(self):
        self.flow_graph = {
            'start': {
                'donator': {
                    'location': {
                        'num_of_servings': {
                            'expiration_day': {
                                'done'
                            }
                        }
                    }
                },
                'receiver': {
                    'location': {
                        'relevant_foods': {}
                    }
                }
            }
        }

    # def get_next_step(self, obj, req):
    #     if obj == None:

    def add_handler(self, action, func):
        self.handlers[action] = func

    def usage(self):
        message = 'Choose one of the following options:\n'
        for idx, handler in enumerate(self.handlers):
            message += f'{idx + 1}- {handler} <number>\n'
        return message

    def action(self, request):
        try:
            # print("REQ")
            for key in request:
                print(key, ":", request[key])
            # for key in request.get('callback_query'):
            #     print(key, request.get('callback_query')[key])
            if 'message' in request:
                if 'location' in request.get('message'):
                    curr_msg = Message({'text': 'location response', 'chat': request.get('message').get('chat')})
                else:
                    curr_msg = Message(request.get('message'))
            else:
                message = {'text': request.get('callback_query').get('message').get('text'),
                           'chat': request.get('callback_query').get('message').get('chat')}
                curr_msg = Message(message)
            action = curr_msg.get_action()
            print("ACTION", action)
            self.handlers.get(action)(curr_msg, request, self.id_obj_map)
            # print('after function')
            # if action == '/location':
            #     data = {"chat_id": curr_msg.get_id(),
            #             "text": "TEST",
            #             "reply_markup": message}
            #     send_post_message(curr_msg.get_id(), 'location', data)
            # else:
            #     send_message(curr_msg.get_id(), message)
        except Exception as e:
            pass


def get_bot():
    bot = Bot()

    bot.add_handler('/start', handlers.handle_choosing_user_type)
    bot.add_handler('/location', handlers.handle_location)
    bot.add_handler('Are you a Donator or Receiver?', handlers.handle_type_answer)
    bot.add_handler('location response', handlers.handle_location_response)

    #bot.add_handler('Please send your location', handlers.handle_location_response)  
    bot.add_handler('The food is good for?', handlers.handle_experation_day_response)
    bot.add_handler('How many people is the meal for?', handlers.handle_num_of_servings_response)

    bot.add_handler('choose your food type', handlers.handle_receiver_food_types_response)
    return bot
