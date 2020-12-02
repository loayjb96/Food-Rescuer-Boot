from location import Location
from geopy.distance import geodesic
from FoodTypes import food_type


class Reciver():
    def __init__(self):
        self.telegram_id = None
        self.telegram_username = None
        self.food_types = []
        self.location = None

    def init_reciver_id(self, id):
        self.telegram_id = id

    def add_receiver_food(self, food):
        if food not in self.food_types:
            self.food_types.append(food)

    def set_location(self, current_location):
        self.location = current_location

    def set_username(self, i_username):
        self.telegram_username = i_username

    def get_relevant_food(self):
        return self.food_types

    def get_relative_distance(self, other_location):
        return geodesic(self.location.get_address(), other_location.get_address()).kilometers

    def add_food_type(self, foodtype):
        print("reciever class: " + foodtype + " is adding ")
        self.food_types.append(foodtype)
        print("reciever class: " + foodtype + " was added ")
        list_of_strings = [str(s) for s in self.food_types]
        print("reciever class: now food has these types:".join(list_of_strings))

    def remove_food_type(self, foodtype):
        print("reciever class: " + foodtype + " is removing ")
        self.food_types.remove(foodtype)
        print("reciever class: " + foodtype + " was removing ")
        list_of_strings = [str(s) for s in self.food_types]
        print("reciever class: now food has these types:".join(list_of_strings))
# res = Reciver()
# loc = location()
# loc2 = location()
# loc.set_address(31.803912232328965, 35.117917594545155)
# loc2.set_address(31.808364038160448, 35.1100292732076)
# res.init_reciver_location(loc.get_address())
# dis = res.get_relative_distance(loc2.get_address())
# print(dis ,'km')
