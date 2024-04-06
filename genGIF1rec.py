import sys
import os
import time
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt, QRect, pyqtSignal
from PyQt5.QtGui import QPixmap, QPainter, QGuiApplication
from PIL import Image

class ScreenshotWindow(QMainWindow):
    screenshotCaptured = pyqtSignal(QPixmap)

    def __init__(self):
        super().__init__()
        self.begin = None
        self.end = None
        self.setWindowOpacity(0.3)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.showFullScreen()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.begin = event.pos()
            self.end = event.pos()
            self.update()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            self.end = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            screen = QGuiApplication.primaryScreen()
            screenshot = screen.grabWindow(0, self.x(), self.y(), self.width(), self.height())
            rect = self.getRect(self.begin, self.end)
            cropped_pixmap = screenshot.copy(rect)
            self.screenshotCaptured.emit(cropped_pixmap)
            self.close()

    def paintEvent(self, event):
        if self.begin is None or self.end is None:
            return

        painter = QPainter(self)
        painter.setPen(Qt.red)
        painter.setBrush(Qt.NoBrush)
        rect = self.getRect(self.begin, self.end)
        painter.drawRect(rect)

    def getRect(self, begin, end):
        x = min(begin.x(), end.x())
        y = min(begin.y(), end.y())
        width = abs(begin.x() - end.x())
        height = abs(begin.y() - end.y())
        return QRect(x, y, width, height)

def capture_and_save_screenshots(rect, num_frames, output_directory, interval):
    for i in range(num_frames):
        screen = QGuiApplication.primaryScreen()
        screenshot = screen.grabWindow(0, rect.x(), rect.y(), rect.width(), rect.height())
        filename = os.path.join(output_directory, f"frame_{i:04d}.png")
        screenshot.save(filename)
        time.sleep(interval)

def create_gif(directory, video_path, frame_rate, duration):
    image_list = [os.path.join(directory, f"frame_{i:04d}.png") for i in range(1, int(frame_rate * duration))]
    image_objects = [Image.open(img) for img in image_list]
    image_objects[0].save(video_path, save_all=True, append_images=image_objects[1:], optimize=False, duration=1.0/float(frame_rate), loop=0)

def save_screenshots(video_path, frame_rate=1, duration=10):
    app = QApplication(sys.argv)
    window = ScreenshotWindow()
    screenshot = None

    def handle_screenshot(pixmap):
        nonlocal screenshot
        screenshot = pixmap

    window.screenshotCaptured.connect(handle_screenshot)
    window.show()
    app.exec_()

    if screenshot:
        num_frames = int(frame_rate * duration)
        interval = 1 / frame_rate
        output_directory = os.path.join(os.path.dirname(video_path), "output")
        os.makedirs(output_directory, exist_ok=True)
        capture_and_save_screenshots(window.getRect(window.begin, window.end), num_frames, output_directory, interval)
        create_gif(output_directory, video_path, frame_rate, duration)

if __name__ == "__main__":
    video_path = "C:\\Users\\wying\\Downloads\\output.gif"
    frame_rate = 10
    duration = 5
    save_screenshots(video_path, frame_rate, duration)
    print(f"GIF saved at {video_path}")
