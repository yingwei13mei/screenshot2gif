import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPixmap, QPainter, QGuiApplication

class ScreenshotWindow(QMainWindow):
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
            cropped_pixmap.save("screenshot.png")
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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ScreenshotWindow()
    window.show()
    sys.exit(app.exec_())
