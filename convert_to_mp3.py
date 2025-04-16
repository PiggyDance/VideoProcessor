from pydub import AudioSegment
import os
import sys


def convert_to_mp3(input_path, output_path=None, bitrate="192k"):
    # 获取文件扩展名
    ext = os.path.splitext(input_path)[1][1:].lower()

    # 使用对应格式加载音频
    try:
        audio = AudioSegment.from_file(input_path, format=ext)
    except Exception as e:
        print(f"加载音频失败: {e}")
        return

    # 如果没有指定输出路径，就使用原始文件名但后缀改为 .mp3
    if output_path is None:
        output_path = os.path.splitext(input_path)[0] + ".mp3"

    try:
        audio.export(output_path, format="mp3", bitrate=bitrate)
        print(f"转换成功: {output_path}")
    except Exception as e:
        print(f"导出 MP3 失败: {e}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python convert_to_mp3.py 输入文件路径 [输出文件路径]")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None

    convert_to_mp3(input_file, output_file)
