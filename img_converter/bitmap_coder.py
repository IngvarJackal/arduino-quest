import sys
import Image
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

if len(sys.argv) != 2:
    print "Specify file for conversion!"
    exit()

im = Image.open(sys.argv[1])
rgb_im = im.convert('RGB')
width, height = im.size

raw = []
for i in range(height):
    for j in range(width):
        r, g, b = rgb_im.getpixel((j, i))
        index = colors.index((r,g,b))
        if index == -1:
            print "ERROR: pixel", r, g, b, "at", i, j, "isn't in the palette!"
            exit()
        else:
            raw.append(index)

with open(sys.argv[1].upper()[:sys.argv[1].find(".")] + ".BIN", "wb") as out:
    binary_data = bitarray.bitarray("".join([bin(width)[2:].zfill(16)] + [bin(x)[2:].zfill(8) for x in raw]))
    binary_data.tofile(out)
