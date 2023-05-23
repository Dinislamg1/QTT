import sys
import cv2
from PyQt5 import uic, QtGui
from PyQt5.QtCore import QTimer, QThread, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
import NS

class VideoThread(QThread):
    frameUpdate = pyqtSignal(QImage)

    def __init__(self, parent=None):
        super(VideoThread, self).__init__(parent)
        self.cap = None

    def setVideoCapture(self, cap):
        self.cap = cap

    def run(self):
        while True:
            ret, img = self.cap.read()
            if not ret:
                break
            h, w, ch = img.shape
            if h > w:
                w = int(w * 501 / h)
                h = 501
            else:
                h = int(h * 501 / w)
                w = 501
            img = cv2.resize(img, (w, h))
            bpl = 3 * w
            qImg = QImage(img.data, w, h, bpl, QImage.Format_BGR888)
            self.frameUpdate.emit(qImg)

            self.msleep(33)

        self.cap.release()

class HandleVideoThread(QThread):
    handleThreadFinished = pyqtSignal()

    def __init__(self, cap, parent=None):
        super(HandleVideoThread, self).__init__(parent)
        self.cap = cap

    def run(self):
        NS.main(self.cap)
        self.handleThreadFinished.emit()

class MyProject(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('Go1.ui', self)
        self.cap = None
        self.cap2 = None
        self.pushButton.clicked.connect(self.getVideo)
        self.pushButton_2.clicked.connect(self.handleVideo)

        self.thread1 = VideoThread(self)
        self.thread1.frameUpdate.connect(self.updateFrame)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.thread1.start)

        self.thread2 = VideoThread(self)
        self.thread2.frameUpdate.connect(self.updateFrame2)
        self.timer2 = QTimer(self)
        self.timer2.timeout.connect(self.thread2.start)

        self.handleThread = HandleVideoThread(None)
        self.handleThread.handleThreadFinished.connect(self.startVideoThread2)

    def handleVideo(self):
        if self.cap is None:
            self.label.setText("Видео не загружено.")
            return

        self.cap2 = cv2.VideoCapture('yolo/examles_pictor/Video4.avi')
        self.thread2.setVideoCapture(self.cap2)

        self.handleThread.cap = self.cap
        self.handleThread.start()

    def startVideoThread2(self):
        self.timer2.start(33)

    def getVideo(self):
        path = QFileDialog.getOpenFileName(self,
                                            "Выбрать видео",
                                            "",
                                            "Файлы видео (*)")[0]

        if not path:
            return
        self.cap = cv2.VideoCapture(path)
        self.thread1.setVideoCapture(self.cap)
        self.timer.start(33)

    def updateFrame(self, qImg):
        self.label.setPixmap(QtGui.QPixmap.fromImage(qImg))

    def updateFrame2(self, qImg):
        self.label_2.setPixmap(QtGui.QPixmap.fromImage(qImg))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyProject()
    ex.show()
    sys.exit(app.exec_())
