import os
import sys
from PIL import Image, ImageFont, ImageDraw
import cv2
import numpy as np
from tqdm import tqdm  # 导入 tqdm

char_list = '`^",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$'
terminal_size = os.get_terminal_size()
width, height = terminal_size.columns, terminal_size.lines


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


def drawImage(ascii_img, width, height):
    font_path = "/usr/share/fonts/TTF/FiraCodeNerdFont-Bold.ttf"
    font_size = 10
    font = ImageFont.truetype(font_path, font_size)

    bbox = font.getbbox("A")
    char_width = bbox[2] - bbox[0]
    char_height = bbox[3] - bbox[1]
    img_width = char_width * width
    img_height = char_height * height
    new_img = Image.new("RGB", (img_width, img_height), (255, 255, 255))
    draw = ImageDraw.Draw(new_img)

    char_cache = {}

    for y in range(height):
        for x in range(width):
            char = ascii_img[y][x]
            if char not in char_cache:
                char_img = Image.new("RGB", (char_width, char_height), (255, 255, 255))
                char_draw = ImageDraw.Draw(char_img)
                char_draw.text((0, 0), char, font=font, fill=(0, 0, 0))
                char_cache[char] = char_img
            else:
                char_img = char_cache[char]
            new_img.paste(char_img, (x * char_width, y * char_height))
    return new_img


img_list = []


def add_to_img_list(new_img):
    img_list.append(new_img)


def convert_img_to_video(img_list, output_video_name, fps):
    first_img = img_list[0]
    open_cv_img = cv2.cvtColor(np.array(first_img), cv2.COLOR_RGB2BGR)
    height, width, _ = open_cv_img.shape

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    output_file_name = output_video_name + ".mp4"
    video = cv2.VideoWriter(output_file_name, fourcc, fps, (width, height))

    for image in img_list:
        open_cv_img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        video.write(open_cv_img)

    video.release()
    # print(f"Video saved as: {output_file_name}")


def Cap_and_Play():
    if len(sys.argv) < 2:
        print("请输入视频地址")
        sys.exit(1)

    videoPath = sys.argv[1]
    videoname, _ = os.path.splitext(os.path.basename(videoPath))

    cap = cv2.VideoCapture(videoPath)
    fps = cap.get(cv2.CAP_PROP_FPS)

    # 获取视频总帧数
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # 使用 tqdm 显示进度条
    with tqdm(total=total_frames, desc="Processing Frames") as pbar:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frame = cv2.flip(frame, 1)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            img = img.resize((width, height))

            ascii_img = convert_to_ascii(img)
            new_img = drawImage(ascii_img, img.width, img.height)
            add_to_img_list(new_img)
            convert_img_to_video(img_list, videoname, fps)

            pbar.update(1)  # 更新进度条

    cap.release()
    cv2.destroyAllWindows()


def main():
    Cap_and_Play()


if __name__ == "__main__":
    main()
