from PIL import Image
import sys
import os
from pathlib import Path

def pixelate_image(image_path, pixel_size):
    # 检查输入图片是否存在
    if not os.path.exists(image_path):
        print(f"图片文件 {image_path} 不存在！")
        sys.exit(1)

    # 打开图片
    img = Image.open(image_path)

    # 获取原始尺寸
    original_size = img.size

    # 缩小图片到像素化尺寸
    img_small = img.resize(
        (original_size[0] // pixel_size, original_size[1] // pixel_size),
        resample=Image.NEAREST
    )

    # 构造输出文件路径
    input_path = Path(image_path)
    output_path = input_path.with_stem(f"{input_path.stem}_pixelated")

    # 保存像素化后的图片（实际像素大小）
    img_small.save(output_path)

    print(f"像素化图片已保存到：{output_path}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("用法: python pixelate_image.py <图片路径> <像素化程度>")
        sys.exit(1)

    image_path = sys.argv[1]  # 输入图片路径
    try:
        pixel_size = int(sys.argv[2])  # 像素化程度
        if pixel_size < 1:
            raise ValueError
    except ValueError:
        print("像素化程度必须是正整数！")
        sys.exit(1)

    # 像素化图片
    pixelate_image(image_path, pixel_size)
