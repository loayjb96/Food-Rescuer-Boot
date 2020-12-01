from message import *
import handlers


class Bot:
    def __init__(self):
        self.flow_graph = {}
        self.handlers = {}
        self.receivers = []
        self.donators = []
        self.build_flow()

    def build_flow(self):
        self.flow_graph = {
            '/start': {
                '/donator': {
                    '/location': {
                        '/num_of_servings': {
                            '/expiration_day': {
                                '/done'
                            }
                        }
                    }
                },
                '/receiver': {
                    '/location': {
                        '/relevant_foods': {}
                    }
                }
            }
        }

    def add_handler(self, action, func):
        self.handlers[action] = func

    def usage(self):
        message = 'Choose one of the following options:\n'
        for idx, handler in enumerate(self.handlers):
            message += f'{idx + 1}- {handler} <number>\n'
        return message

    def action(self, request):
        try:
            print("REQ", request)
            curr_msg = Message(request.get('message'))
            print(request.get('message'))
            action = curr_msg.get_action()

            message = ''
            if action not in self.handlers:
                message = self.usage()
            else:
                number = curr_msg.get_params()
                message = self.handlers.get(action)(number)
            print('after function')
            if action == '/location':
                data = {"chat_id": curr_msg.get_id(),
                        "text": "TEST",
                        "reply_markup": message}
                send_post_message(curr_msg.get_id(), 'location', data)
            else:
                send_message(curr_msg.get_id(), message)
        except Exception as e:
            pass


def get_bot():
    bot = Bot()

    bot.add_handler('/type_choose', handlers.handle_choosing_user_type)
    bot.add_handler('/location', handlers.get_location)
    return bot
