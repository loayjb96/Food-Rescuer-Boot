from datetime import datetime, timedelta, date


class Food:
    def __init__(self):
        self.m_food_id = ""
        self.m_food_types = set()
        self.m_donator = ""
        self.m_photos = ""
        self.m_number_of_servings = 0
        self.m_expiration_date = ""  # datetime.date.today()
        self.m_description = ""

    def set_experation_day_in_x_days(self, i_days):
        self.m_expiration_date = (datetime.now() + timedelta(days=i_days))

    def set_number_of_servings(self,serving_size):
        self.m_number_of_servings = serving_size

    def add_food_type(self, foodtype):
        print("food class: " + foodtype + " is adding ")
        self.m_food_types.add(foodtype)
        print("food class: " + foodtype + " was added ")
        list_of_strings = [str(s) for s in self.m_food_types]
        print("food class: now food has these types:".join(list_of_strings) )
 
    def remove_food_type(self,foodtype):
        print("food class: " + foodtype + " is removing ")
        self.m_food_types.remove(foodtype)
        print("food class: " + foodtype + " was removing ")
        list_of_strings = [str(s) for s in self.m_food_types]
        print("food class: now food has these types:".join(list_of_strings))
