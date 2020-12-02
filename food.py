from datetime import datetime, timedelta, date


class Food:
    def __init__(self):
        self.m_food_id = ""
        self.m_food_types = []
        self.m_donator = ""
        self.m_photos = ""
        self.m_number_of_servings = 0
        self.m_expiration_date = ""  # datetime.date.today()
        self.m_description = ""

    def set_experation_day_in_x_days(self, i_days):
        self.m_expiration_date = (datetime.now() + timedelta(days=i_days))

    def set_number_of_servings(self,serving_size):
        self.m_number_of_servings = serving_size

    def add_food_type(self, food):
        self.food_types.add(food)
 
  
