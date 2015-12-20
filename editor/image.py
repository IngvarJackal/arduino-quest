import bitarray
from Tkinter import *
import tkMessageBox

from math import sin

PHOTO_IMAGE = None

COLORS = [
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

def set_pixel(color, coords, img):
    for i in range(4):
        for j in range(4):
            img.put("#"+"".join([hex(x)[2:] for x in color]), (coords[0]*4+i, coords[1]*4+j))

LEN_OFFSET = 16
def decode_binary_data(data):
    result = []
    i = int("".join(["1" if x else "0" for x in data[:LEN_OFFSET]]), 2)
    for a, b, c, d, e in zip(data[3+LEN_OFFSET:][::8], data[4+LEN_OFFSET:][::8], data[5+LEN_OFFSET:][::8], data[6+LEN_OFFSET:][::8], data[7+LEN_OFFSET:][::8]):
        result.append(int("".join(["1" if x else "0" for x in [a,b,c,d,e]]), 2))
    return i, result

def load_image(image):
    with open(image, "rb") as imgfile:
        arr = bitarray.bitarray()
        arr.fromfile(imgfile)
        return decode_binary_data(arr)

def draw_image(l, image_data, canvas):
    global PHOTO_IMAGE
    WIDTH = canvas.winfo_reqwidth()-2
    HEIGHT = canvas.winfo_reqheight()-2
    
    if WIDTH*HEIGHT/16 != len(image_data):
        print "expected", WIDTH*HEIGHT/16, "got", len(image_data), "pixels!"
        tkMessageBox.showwarning("", "Wrong image resolution!")
        return False
    else:        
        PHOTO_IMAGE = PhotoImage(width=WIDTH, height=HEIGHT)
        canvas.create_image((WIDTH/2, HEIGHT/2), image=PHOTO_IMAGE, state="normal")

        row = 0
        col = 0
        for i in image_data:
            set_pixel(COLORS[i], (col, row), PHOTO_IMAGE)
            col += 1
            if col >= l:
                col = 0
                row += 1
        return True
