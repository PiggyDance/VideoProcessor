# -*- encoding: utf-8 -*-

import os
import sys
from moviepy.editor import VideoFileClip
from pydub import AudioSegment
import speech_recognition as sr

'''
 python extract_mp3_txt.py /Volumes/disk/tmp/wang_zhian.mp4 2300 7000
'''

def extract_audio_clip(input_video, start_ms, end_ms):
    # 计算开始和结束的秒数
    start_sec = start_ms / 1000
    end_sec = end_ms / 1000

    # 加载视频文件
    clip = VideoFileClip(input_video).subclip(start_sec, end_sec)

    # 导出为 wav 临时音频文件
    temp_wav = "temp_audio.wav"
    clip.audio.write_audiofile(temp_wav, codec='pcm_s16le')

    # 转换为 mp3
    mp3_filename = f"{start_ms}_{end_ms}.mp3"
    audio = AudioSegment.from_wav(temp_wav)
    audio.export(mp3_filename, format="mp3")

    # 删除临时 wav 文件
    os.remove(temp_wav)
    return mp3_filename

def transcribe_audio_to_text(mp3_file, txt_file):
    # 读取 mp3 并转换为 wav（speech_recognition 只支持 wav）
    sound = AudioSegment.from_mp3(mp3_file)
    temp_wav = "temp_for_recognition.wav"
    sound.export(temp_wav, format="wav")

    # 初始化语音识别器
    recognizer = sr.Recognizer()
    with sr.AudioFile(temp_wav) as source:
        audio_data = recognizer.record(source)

        try:
            text = recognizer.recognize_google(audio_data, language="zh-CN")  # 可根据需要换成英文等
        except sr.UnknownValueError:
            text = "[无法识别音频中的文字]"
        except sr.RequestError as e:
            text = f"[语音识别请求失败: {e}]"

    # 写入文本文件
    with open(txt_file, 'w', encoding='utf-8') as f:
        f.write(text)

    # 删除临时 wav
    os.remove(temp_wav)

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("用法: python script.py 视频文件 开始毫秒 结束毫秒")
        print("例如: python script.py input.mp4 1000 4560")
        sys.exit(1)

    input_video = sys.argv[1]
    start_ms = int(sys.argv[2])
    end_ms = int(sys.argv[3])

    mp3_filename = extract_audio_clip(input_video, start_ms, end_ms)
    txt_filename = mp3_filename.replace('.mp3', '.txt')
    transcribe_audio_to_text(mp3_filename, txt_filename)

    print(f"音频保存为: {mp3_filename}")
    print(f"识别结果保存为: {txt_filename}")
