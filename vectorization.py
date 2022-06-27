from typing import List
from pixel import Pixel
from codeWord import CodeWord
import math
class Vectorization():
    def __init__(self):
        self.code_words = []
        self.epsilon = 0.01
        self.pixels = []
    
    def create_codebook(self,pixels: List[Pixel], size_codebook ):
        size = len(pixels)
        # główny - środkowy wektor zbioru
        blue, green, red = 0,0,0
        for p in pixels:
            blue += p.blue
            green += p.green
            red += p.red
        x = Pixel(blue / size, green/size, red/size)
        code_word = CodeWord(x)
        self.code_words.append(code_word)
        self.pixels = pixels
        # średnia odległość od głownego wektora

        average_distance = 0
        for p in pixels:
            average_distance += p.get_distance_to_pixel(code_word.main_word) 
        average_distance /= len(pixels)

        while len(self.code_words) < size_codebook:
            # zwiększenie kolekcji o piksele odległości epsilon
            self.increase_collection()
            
            # algorytm
            average_distance = self.LBG_algorithm(average_distance)
        #zwracamy nasze piksele główne
        return self.code_words
        
    

    def increase_collection(self):
        code_words = []
        
        for cw in self.code_words:
            # mnożenie parametrow b g r codewordów   o 1 +/- epsilon, zwiększamy ich ilość o *2, pozbywamy się starych 
            word1 = CodeWord(cw.main_word.get_scaled_vector(1 + self.epsilon))
            code_words.append(word1)
            word2 = CodeWord(cw.main_word.get_scaled_vector(1 - self.epsilon))
            code_words.append(word2)
        self.code_words = code_words
        

    def LBG_algorithm(self, init_avg_distance) -> float:
        avg_distance = 0.0
        err = 1.0 + self.epsilon

        while err > self.epsilon:
            # usuwamy najbliższe piksele do piksela cw 
            for cw in self.code_words: 
                cw.remove_all_members()
            # klasteryzacja dodajemy do każdego cw liste pikseli, dla których cw jest najbliżej
            self.clusterization()
            # dla zbioru sąsiadów każdego cw generujemy nowy cw licząc średnią dla pikseli zbliżonych do cw 
            self.generate_centroid()
            if avg_distance > 0:
                before_distance = avg_distance
            else:
                before_distance = init_avg_distance
            # średni dystans dla najbliższych pikseli do cw - średni błąd kwantyzacji
            avg_distance = self.quantization_error()
            err = (before_distance - avg_distance) / before_distance
        return avg_distance

    def clusterization(self):
        reset = math.pow(2, 24)
        for pixel in self.pixels:
            shortest = reset
            idx = 0
            for i, cw in enumerate(self.code_words):
                distance = pixel.get_distance_to_pixel(cw.main_word)
                if distance < shortest:
                    shortest = distance
                    idx = i
            self.code_words[idx].add_new_pixel(pixel)

    def generate_centroid(self):
        for cw in self.code_words:
            if len(cw.nearest_members) > 0:
                new_matched_cw = middle_vector(cw.nearest_members)
                cw.update_code_word(new_matched_cw)

    def quantization_error(self) -> float:
        err: float = 0.0
        for cw in self.code_words:
            for pixel in cw.nearest_members:
                err += (cw.main_word.get_distance_to_pixel(pixel) / len(self.pixels))
        return err



def middle_vector(pixels):
    size = len(pixels)
    blue, green, red = 0,0,0
    for p in pixels:
        blue += p.blue
        green += p.green
        red += p.red
    return Pixel(blue /size, green/size, red/size)

    