# 指定间隔时间提取视频帧
# python extract_frames.py <视频路径> <间隔时间（毫秒）>

import os
import subprocess
import sys
from pathlib import Path

def extract_frames(video_path, interval_ms):
    # 检查视频文件是否存在
    if not os.path.exists(video_path):
        print(f"视频文件 {video_path} 不存在！")
        return

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
    except subprocess.CalledProcessError as e:
        print(f"FFmpeg 执行失败：{e}")

if __name__ == "__main__":
    # 从命令行获取参数
    if len(sys.argv) != 3:
        print("用法: python extract_frames.py <视频路径> <间隔时间（毫秒）>")
        sys.exit(1)

    video_path = sys.argv[1]  # 视频路径
    try:
        interval_ms = int(sys.argv[2])  # 帧提取间隔时间
    except ValueError:
        print("间隔时间必须是整数（毫秒）！")
        sys.exit(1)

    # 调用帧提取函数
    extract_frames(video_path, interval_ms)
