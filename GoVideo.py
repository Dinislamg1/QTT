import sys

import cv2
from PyQt5 import uic, QtGui
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
import NS, BDview
from BDview import Ui_MainWindow

class MyProject(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('Go1.ui', self)
        self.cap = None
        self.cap2 = None
        self.pushButton.clicked.connect(self.getVideo)
        self.pushButton_2.clicked.connect(self.HandleVideo)#!!!!!!
        self.pushButton_3.clicked.connect(self.OpenBD)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateFrame)
        self.timer2 = QTimer(self)
        self.timer2.timeout.connect(self.updateFrame2)
        # BDview.Ui_MainWindow.main(self)


    def OpenBD(self):
        self.BDview = Ui_MainWindow()
        self.BDview.show()

    def HandleVideo(self):
        if self.cap is None:
            self.label.setText("Видео не загружено.")
            return
        NS.main(self.cap)
        self.cap2 = cv2.VideoCapture('yolo/examles_pictor/Video5.avi')
        self.timer2.start(33)

    def getVideo(self):
        path = QFileDialog.getOpenFileName(self,
                                            "Выбрать видео",
                                            "",
                                            "Файлы видео (*)")[0]

        if not path:
            return
        self.cap = cv2.VideoCapture(path)
        self.timer.start(33)

    def updateFrame(self):
        ret, img = self.cap.read()
        if not ret:
            self.timer.stop()
            self.cap.release()
            return
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
        self.label.setPixmap(QtGui.QPixmap.fromImage(qImg))

    def updateFrame2(self):
        ret, img = self.cap2.read()
        if not ret:
            self.timer2.stop()
            self.cap2.release()
            return
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
        self.label_2.setPixmap(QtGui.QPixmap.fromImage(qImg))


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = MyProject()
    ex.show()
    sys.exit(app.exec_())
