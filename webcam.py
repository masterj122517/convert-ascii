import os
from PIL import Image
import cv2

char_list = '`^",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$'


def get_average(pixel_martix, width, height):
    brightness_martix = []
    for y in range(height):
        row = []
        for x in range(width):
            p = pixel_martix[y][x]
            result = 0.21 * p[0] + 0.72 * p[1] + 0.07 * p[2]
            row.append(result)
        brightness_martix.append(row)
    return brightness_martix


def convert_to_ascii(img):
    width = img.width
    height = img.height
    pixel_martix = [[img.getpixel((x, y)) for x in range(width)] for y in range(height)]
    brightness_martix = get_average(pixel_martix, width, height)
    ascii_img = []
    for y in range(height):
        row = []
        for x in range(width):
            index = min(
                brightness_martix[y][x] * (len(char_list) - 1) // 255,
                len(char_list) - 1,
            )
            row.append(char_list[int(index)])
        ascii_img.append(row)
    return ascii_img


def display_ascii(ascii_img):
    for line in ascii_img:
        print("".join(line))


terminal_size = os.get_terminal_size()
width, height = terminal_size.columns, terminal_size.lines

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.flip(frame, 1)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(frame)
    # img.thumbnail((90, 85))
    img = img.resize(
        (width, height)
    )  # use the full size of the terminal emulator but could cost bad apprence
    ascii_img = convert_to_ascii(img)
    display_ascii(ascii_img)

cap.release()
cv2.destoryAllWindows()
