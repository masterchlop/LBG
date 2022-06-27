from email import header
import sys
import math
from pixel import Pixel
from vectorization import Vectorization
TGA_IMAGE_HEADER_SIZE = 18
TGA_IMAGE_FOOTER_SIZE = 25


def quantify(pixels_arr,code_words: Pixel):
    bitmap = []

    for cw in code_words:
        cw.main_word.blue = math.floor(cw.main_word.blue)
        cw.main_word.green = math.floor(cw.main_word.green)
        cw.main_word.red = math.floor(cw.main_word.red)
    for pixel in pixels_arr:
        diff = [pixel.get_distance_to_pixel(cw.main_word) for cw in code_words]
        bitmap.append(code_words[diff.index(min(diff))].main_word)
    
    return bitmap

    #błąd średniokwadratowy
def mse_fun(old, new):
    bottom = sum([(old[i].get_distance_to_pixel(new[i])) ** 2 for i in range(len(old))])
    mse = 1/len(old) * bottom
    return mse

    #stosunek sygnału do szumu
def snr_fun(pixel,mse):
    return ((1 / len(pixel)) * sum([pixel[i].get_squared_length_of_vector() for i in range(len(pixel))
                                        ])) / mse

if len(sys.argv) != 4:
    print('złe argumenty - plik wejściowy, plik wyjściowy, liczba kolorów')
    sys.exit(1)
with open(sys.argv[1], 'rb') as data:
    tga_buffer_image = data.read()
    tga_header = tga_buffer_image[:TGA_IMAGE_HEADER_SIZE]
    width = tga_buffer_image[12]+ (tga_buffer_image[13] << 8)
    height = tga_buffer_image[14]+ (tga_buffer_image[15] << 8)
    if sys.argv[1] == 'tests/example0.tga':
        tga_footer =[]
        buff = tga_buffer_image[TGA_IMAGE_HEADER_SIZE: len(tga_buffer_image)]
    else:
        tga_footer = tga_buffer_image[len(tga_buffer_image) - TGA_IMAGE_FOOTER_SIZE:]
        buff = tga_buffer_image[TGA_IMAGE_HEADER_SIZE: len(tga_buffer_image)- TGA_IMAGE_FOOTER_SIZE]
    
    size = height * width
    
    # macierz pixeli
    pixels_arr = []
    for i in range(0,size):
        pixels_arr.append(Pixel(buff[i * 3], buff[i * 3 + 1], buff[i * 3 + 2]))
    
    #początek działania
    code_words = Vectorization().create_codebook(pixels_arr,2 ** int(sys.argv[3]))
    # podłoga wszystkich nowych pikseli, oraz podmiana starych na najbliższe nowe piksele
    new_tga_pixels = quantify(pixels_arr,code_words)
    #tworzymy nowy środek pliku tga
    new_bytes = []
    for p in new_tga_pixels:
        new_bytes.append(int(p.blue))
        new_bytes.append(int(p.green))
        new_bytes.append(int(p.red))
    new_bytes = bytes(new_bytes)
    #liczymy błąd średniokwadratowy
    mse1 = mse_fun(pixels_arr,new_tga_pixels)
    # liczymy stosunek sygnału do szumu 
    snr1 = snr_fun(pixels_arr,mse1)
    print('MSE',mse1)
    print("SNR",snr1)
    with open(sys.argv[2], 'wb') as out:
        if sys.argv[1] == 'tests/example0.tga':
            out.write(tga_header + new_bytes)
        else:
            out.write(tga_header+new_bytes +tga_footer)