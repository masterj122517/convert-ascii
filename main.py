from PIL import Image, ImageFont, ImageDraw
import os


imgPath = input("please give the path of the img ")
imgName = os.path.basename(imgPath)
img = Image.open(imgPath)
size = (450, 450)
img.thumbnail(size)

width = img.width
height = img.height
pixel_matrix = [[img.getpixel((x, y)) for x in range(width)] for y in range(height)]
brightness_martix = []


# def get_average(pixel_matrix, brightness_martix):
#     brightness_martix = [
#         [sum(pixel_matrix[y][x]) // 3 for x in range(width)] for y in range(height)
#     ]
#     return brightness_martix


def get_average(pixel_matrix, brightness_martix):
    for y in range(height):
        row = []
        for x in range(width):
            p = pixel_matrix[y][x]
            result = 0.21 * p[0] + 0.72 * p[1] + 0.07 * p[2]
            row.append(int(result))
        brightness_martix.append(row)
    return brightness_martix


brightness_martix = get_average(pixel_matrix, brightness_martix)

char_list = '`^",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$'
new_img = [[" " for x in range(width)] for y in range(height)]

for y in range(height):
    for x in range(width):
        # index = brightness_martix[y][x] * (len(char_list) - 1) // 255
        index = min(
            brightness_martix[y][x] * (len(char_list) - 1) // 255, len(char_list) - 1
        )
        new_img[y][x] = char_list[index]


# for line in new_img:
#     print("".join(line))

# 创建一个新的图像，用于保存ASCII图像
font_path = "/usr/share/fonts/TTF/FiraCodeNerdFont-Bold.ttf"  # 字体路径
font_size = 10
font = ImageFont.truetype(font_path, font_size)
bbox = font.getbbox("A")  # 获取字符的边界框 (left, top, right, bottom)
char_width = int(bbox[2] - bbox[0])
char_height = int(bbox[3] - bbox[1])
img_width = int(char_width * width)
img_height = int(char_height * height)
ascii_img = Image.new("RGB", (img_width, img_height), (255, 255, 255))  # 白色背景
draw = ImageDraw.Draw(ascii_img)

# 将字符矩阵绘制到图像上
for y in range(height):
    for x in range(width):
        draw.text(
            (x * char_width, y * char_height), new_img[y][x], font=font, fill=(0, 0, 0)
        )

# 保存为图像文件
save_path = os.path.join("./converted_img", imgName)
ascii_img.save(save_path)
print("ASCII图像已保存为 " + imgName)
