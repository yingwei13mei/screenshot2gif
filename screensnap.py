import cv2
import os
from PIL import Image
import time
import pyscreenshot
from pyscreenshot import grab

import pyautogui
from PIL import ImageGrab

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPixmap, QPainter, QGuiApplication


#捕捉屏幕的函数
def capture_screen(region=None):
    if region:
        return pyscreenshot.grab(region)
    else:
        return pyscreenshot.grab()

# 将屏幕截图保存为图片序列
def save_screenshots(video_path, frame_rate=1, duration=10):
    # 计算需要保存的帧数
    num_frames = int(frame_rate * duration)
    # 计算帧之间的时间间隔（秒）
    interval = 1 / frame_rate

    # 保存图片序列
    for i in range(num_frames):
        screenshot = capture_screen()
        filename = f"frame_{i:04d}.png"
        screenshot.save(filename)
        time.sleep(interval)

    # 创建GIF
    create_gif(os.path.join(os.path.dirname(video_path), "output"), video_path, frame_rate, duration)

# 使用Pillow创建GIF
def create_gif(directory, video_path, frame_rate, duration):
    # 构建图片文件列表
    image_list = [os.path.join(directory, f"frame_{i:04d}.png") for i in range(1, frame_rate * duration)]
    # 将图片列表转换为Image对象列表
    image_objects = [Image.open(img) for img in image_list]
    # 保存GIF
    image_objects[0].save(video_path, save_all=True, append_images=image_objects[1:], optimize=False, duration=1.0/float(frame_rate), loop=0)

# 主函数
def main():
    video_path = "C:\\Users\\wying\\Downloads\\output.gif"  # 输出的GIF文件路径
    frame_rate = 10  # GIF的帧率（FPS）
    duration = 5  # 录制视频的时长（秒）

    # 确保输出目录存在
    os.makedirs(os.path.join(os.path.dirname(video_path), "output"), exist_ok=True)
    os.chdir(os.path.join(os.path.dirname(video_path), "output"))
    
    # 开始录制屏幕
    save_screenshots(video_path, frame_rate, duration)

    print(f"GIF saved at {video_path}")

if __name__ == "__main__":
    main()
