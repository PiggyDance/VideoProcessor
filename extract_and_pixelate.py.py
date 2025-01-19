# 提取像素
# python extract_and_pixelate.py <视频路径> <间隔时间（毫秒）> <像素化程度>

import os
import subprocess
import sys
from pathlib import Path
from PIL import Image

def extract_frames(video_path, interval_ms):
    # 检查视频文件是否存在
    if not os.path.exists(video_path):
        print(f"视频文件 {video_path} 不存在！")
        sys.exit(1)

    # 获取视频文件名（不含扩展名）
    video_name = Path(video_path).stem

    # 创建输出目录
    output_dir = f"{video_name}_frames"
    os.makedirs(output_dir, exist_ok=True)

    # 设置帧提取间隔
    interval_seconds = interval_ms / 1000

    # 构建 FFmpeg 命令
    output_pattern = os.path.join(output_dir, f"{video_name}_frame_%05d.png")
    command = [
        "ffmpeg",
        "-i", video_path,                # 输入视频
        "-vf", f"fps=1/{interval_seconds}",  # 设置帧率（间隔时间）
        "-q:v", "2",                     # 设置输出图片质量（2 表示高质量）
        output_pattern                   # 输出图片命名规则
    ]

    # 调用 FFmpeg
    try:
        subprocess.run(command, check=True)
        print(f"帧提取完成！图片保存在：{output_dir}")
        return output_dir
    except subprocess.CalledProcessError as e:
        print(f"FFmpeg 执行失败：{e}")
        sys.exit(1)

def pixelate_image(image_path, pixel_size, output_path):
    # 打开图片
    img = Image.open(image_path)

    # 获取原始尺寸
    original_size = img.size

    # 缩小图片到像素化尺寸
    img_small = img.resize(
        (original_size[0] // pixel_size, original_size[1] // pixel_size),
        resample=Image.NEAREST
    )

    # 保存像素化后的图片（实际像素大小）
    img_small.save(output_path)

def pixelate_frames(frames_dir, pixel_size):
    # 创建像素化后的输出目录
    pixelated_dir = f"{frames_dir}_pixelated"
    os.makedirs(pixelated_dir, exist_ok=True)

    # 遍历所有帧图片
    for frame_file in os.listdir(frames_dir):
        if frame_file.endswith(".png"):
            input_path = os.path.join(frames_dir, frame_file)
            output_path = os.path.join(pixelated_dir, frame_file)

            # 像素化图片
            pixelate_image(input_path, pixel_size, output_path)

    print(f"像素化完成！图片保存在：{pixelated_dir}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("用法: python script.py <视频路径> <间隔时间（毫秒）> <像素化程度>")
        sys.exit(1)

    video_path = sys.argv[1]  # 视频路径
    try:
        interval_ms = int(sys.argv[2])  # 帧提取间隔时间
        pixel_size = int(sys.argv[3])  # 像素化程度
        if pixel_size < 1:
            raise ValueError
    except ValueError:
        print("间隔时间和像素化程度必须是正整数！")
        sys.exit(1)

    # 提取帧
    frames_dir = extract_frames(video_path, interval_ms)

    # 像素化帧
    pixelate_frames(frames_dir, pixel_size)
