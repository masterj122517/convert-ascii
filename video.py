import os
import sys
from PIL import Image
import cv2
from moviepy.editor import VideoFileClip
import pygame

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


# 获取终端大小
terminal_size = os.get_terminal_size()
width, height = terminal_size.columns, terminal_size.lines

# 检查输入视频路径
if len(sys.argv) < 2:
    print("请输入视频地址")
    sys.exit(1)

videoPath = sys.argv[1]

clip = VideoFileClip(videoPath)
audio_path = "temp_audio.wav"
clip.audio.write_audiofile(audio_path)

pygame.mixer.init()
pygame.mixer.music.load(audio_path)
pygame.mixer.music.play()

cap = cv2.VideoCapture(videoPath)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.flip(frame, 1)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(frame)
    img = img.resize((width, height))

    ascii_img = convert_to_ascii(img)
    display_ascii(ascii_img)

    # 检查音频播放状态，播放完退出
    if not pygame.mixer.music.get_busy():
        break

# 释放资源
cap.release()
pygame.mixer.music.stop()
pygame.quit()
os.remove(audio_path)
cv2.destroyAllWindows()
