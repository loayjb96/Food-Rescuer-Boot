class Location():
    def __init__(self):
        self.longitude = None
        self.latitude = None

    def get_address(self):
        return self.longitude, self.latitude

    def set_address(self, x, y):
        self.latitude = x
        self.longitude = y

    def __str__(self):
        return f"({self.longitude}, {self.latitude})"
