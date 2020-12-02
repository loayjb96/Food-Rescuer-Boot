from food import Food


class Donator:
    def __init__(self):
        self.m_id = ""
        self.m_donator_level = 0.5
        self.m_telegram_username = None
        self.m_location = ""
        self.m_open_foods = ""
        self.m_food_being_built = Food()
        self.user_name = None
        self.m_donation_counter = 1
        self.photos = set()

    def set_location(self, location):
        self.m_location = location
    def set_username(self,i_username):
        self.m_telegram_username = i_username
    def set_id(self, i_id):
        self.m_id = i_id
