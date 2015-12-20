import pygame
import sys
from time import sleep
import bitarray

colors = [
    (0, 0, 0),
    (34, 32, 52),
    (69, 40, 60),
    (102, 57, 49),
    (143, 86, 59),
    (223, 113, 38),
    (217, 160, 102),
    (238, 195, 154),
    (251, 242, 54),
    (153, 229, 80),
    (106, 190, 48),
    (55, 148, 110),
    (75, 105, 47),
    (82, 75, 36),
    (50, 60, 57),
    (63, 63, 116),
    (48, 96, 130),
    (91, 110, 225),
    (99, 155, 255),
    (95, 205, 228),
    (203, 219, 252),
    (255, 255, 255),
    (155, 173, 183),
    (132, 126, 135),
    (105, 106, 106),
    (89, 86, 82),
    (118, 66, 138),
    (172, 50, 50),
    (217, 87, 99),
    (215, 123, 186),
    (143, 151, 74),
    (138, 111, 48)
]

pygame.init()

screen = pygame.display.set_mode((720,480))

screen.fill(colors[0])

def set_pixel(color, coords):
    for i in range(3):
        for j in range(3):
            screen.set_at((coords[0]*3+i, coords[1]*3+j), color)

def process_events():
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                exit()
            if event.key == pygame.K_RIGHT:
                exit()

LEN_OFFSET = 16
def decode_binary_data(data):
    result = []
    i = int("".join(["1" if x else "0" for x in data[:LEN_OFFSET]]), 2)
    for a, b, c, d, e in zip(data[0+LEN_OFFSET:][::5], data[1+LEN_OFFSET:][::5], data[2+LEN_OFFSET:][::5], data[3+LEN_OFFSET:][::5], data[4+LEN_OFFSET:][::5]):
        result.append(int("".join(["1" if x else "0" for x in [a,b,c,d,e]]), 2))
    return i, result

def load_image(image):
    with open(image, "rb") as imgfile:
        arr = bitarray.bitarray()
        arr.fromfile(imgfile)
        return decode_binary_data(arr)

def draw_image(l, image):
    row = 0
    col = 0
    for i in image:
        set_pixel(colors[i], (col, row))
        col += 1
        if col >= l:
            col = 0
            row += 1
    
    pygame.display.update()

i, img = load_image("SAMPLE.BIN")

draw_image(i, img)

while True:
    process_events()
    sleep(0.05)
