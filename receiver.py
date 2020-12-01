from location import Location
from geopy.distance import geodesic
from FoodTypes import food_type


class Reciver():
    def __init__(self):
        self.telegram_id = None
        self.food_types = []
        self.location = None

    def init_reciver_id(self, id):
        self.telegram_id = id

    def init_receiver_food(self, food):
        for item in food:
            self.food_types.append(item)

    def set_location(self, current_location):
        self.location = current_location

    def get_relevant_food(self):
        return self.food_types

    def get_relative_distance(self, other_location):
        return geodesic(self.location, other_location).kilometers

# res = Reciver()
# loc = location()
# loc2 = location()
# loc.set_address(31.803912232328965, 35.117917594545155)
# loc2.set_address(31.808364038160448, 35.1100292732076)
# res.init_reciver_location(loc.get_address())
# dis = res.get_relative_distance(loc2.get_address())
# print(dis ,'km')
