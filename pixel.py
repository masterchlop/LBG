import math

class Pixel:

    def __init__(self, blue: float, green: float, red: float):
        self.blue = blue
        self.green = green
        self.red = red

    
    def get_distance_to_pixel(self, pixel: 'Pixel') -> float:
        return math.pow(self.blue - pixel.blue, 2) + math.pow(self.green - pixel.green, 2) + math.pow(
            self.red - pixel.red, 2)

    def get_scaled_vector(self, epsilon: float) -> 'Pixel':
        return Pixel(self.blue * epsilon, self.green * epsilon, self.red * epsilon)

    def flor_vectors(self) -> 'Pixel':
        self.blue = math.floor(self.blue)
        self.green = math.floor(self.green)
        self.red = math.floor(self.red)
        return self

    def get_squared_length_of_vector(self):
        return math.pow(self.blue, 2) + math.pow(self.green, 2) + math.pow(
            self.red, 2)