# 移除背景抠出人物,并像素化
# python pixelate_and_remove_bg.py <图片路径> <像素化程度>

from PIL import Image
from rembg import remove
import sys
import os
from pathlib import Path
from io import BytesIO

def remove_background(image_path):
    """
    使用 rembg 去除图片背景。
    """
    # 打开图片并去除背景
    with open(image_path, "rb") as file:
        input_image = file.read()
        output_image = remove(input_image)

    # 加载去除背景后的图片
    img_no_bg = Image.open(BytesIO(output_image)).convert("RGBA")
    return img_no_bg

def pixelate_image(img, pixel_size):
    """
    对图片进行像素化处理。
    """
    # 获取图片原始尺寸
    original_size = img.size

    # 缩小图片到像素化尺寸
    img_small = img.resize(
        (original_size[0] // pixel_size, original_size[1] // pixel_size),
        resample=Image.NEAREST
    )

    # 放大图片回原尺寸（保持像素化效果）
    img_pixelated = img_small.resize(original_size, resample=Image.NEAREST)
    return img_pixelated

def process_image(image_path, pixel_size):
    """
    去除背景并像素化图片。
    """
    # 检查输入图片是否存在
    if not os.path.exists(image_path):
        print(f"图片文件 {image_path} 不存在！")
        sys.exit(1)

    # 去除背景
    img_no_bg = remove_background(image_path)

    # 对图片进行像素化处理
    img_pixelated = pixelate_image(img_no_bg, pixel_size)

    # 构造输出文件路径
    input_path = Path(image_path)
    output_path = input_path.with_stem(f"{input_path.stem}_pixelated")

    # 保存像素化后的图片
    img_pixelated.save(output_path, "PNG")
    print(f"像素化图片已保存到：{output_path}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("用法: python pixelate_and_remove_bg.py <图片路径> <像素化程度>")
        sys.exit(1)

    image_path = sys.argv[1]  # 输入图片路径
    try:
        pixel_size = int(sys.argv[2])  # 像素化程度
        if pixel_size < 1:
            raise ValueError
    except ValueError:
        print("像素化程度必须是正整数！")
        sys.exit(1)

    # 处理图片
    process_image(image_path, pixel_size)