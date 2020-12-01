from food import Food


class Donator:
    def __init__(self):
        self.m_id = ""
        self.m_donator_level = ""
        self.m_location = ""
        self.m_open_foods = ""
        self.m_food_being_built = Food()
        self.m_donation_counter = ""

    def set_location(self, location):
        self.m_location = location

    def set_id(self, i_id):
        self.m_id = i_id
