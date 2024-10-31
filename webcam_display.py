import cv2
from PIL import Image
import numpy as np
import subprocess
import os

# 字符集
char_list = '`^",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$'


def get_average(pixel_matrix, width, height):
    brightness_matrix = []
    for y in range(height):
        row = []
        for x in range(width):
            p = pixel_matrix[y][x]
            result = 0.21 * p[0] + 0.72 * p[1] + 0.07 * p[2]
            row.append(int(result))
        brightness_matrix.append(row)
    return brightness_matrix


def convert_to_ascii(img):
    width, height = img.size
    pixel_matrix = [[img.getpixel((x, y)) for x in range(width)] for y in range(height)]
    brightness_matrix = get_average(pixel_matrix, width, height)

    new_img = [[" " for x in range(width)] for y in range(height)]
    for y in range(height):
        for x in range(width):
            index = min(
                brightness_matrix[y][x] * (len(char_list) - 1) // 255,
                len(char_list) - 1,
            )
            new_img[y][x] = char_list[index]

    return new_img


def display_ascii_art(ascii_img):
    os.system("clear")  # 清除终端内容
    for row in ascii_img:
        print("".join(row))


# 捕获实时视频流
cap = cv2.VideoCapture(0)  # 0 表示默认摄像头

# subprocess.Popen(["vlc", "v4l2:///dev/video0"])  # 对于 Linux 系统

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 转换为 PIL 图像
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # 转换颜色空间
    img = Image.fromarray(frame)
    img.thumbnail((80, 80))  # 调整图像大小以适应终端

    ascii_img = convert_to_ascii(img)
    display_ascii_art(ascii_img)  # 显示字符图像

    # 按 'q' 键退出
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
