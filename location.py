
class location():
    def __init__(self):
        self.Longtitude = None
        self.Latitude = None

    def get_address(self):
        return(self.Longtitude,self.Latitude)

    def set_address(self, x, y):
        self.Latitude = x
        self.Longtitude = y
