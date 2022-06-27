from mimetypes import init
from pixel import Pixel


class CodeWord:
    def __init__(self,pixel):
        self.nearest_member = []
        self.main_word: Pixel = pixel

    def remove_all_members(self):
        self.nearest_members = []

    def add_new_pixel(self, pixel: Pixel):
        self.nearest_members.append(pixel)

    def update_code_word(self, new_state: Pixel):
        self.main_word = new_state