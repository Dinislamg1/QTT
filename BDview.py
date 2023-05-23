# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'BDview.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
import sqlite3

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QVBoxLayout


class Ui_MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.resize(800,600)

        self.centralwidget = QtWidgets.QWidget(self)

        self.centralwidget.setObjectName("centralwidget")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(10, 20, 781, 351))
        self.tableWidget.setRowCount(100)
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setColumnWidth(0, 75)
        self.tableWidget.setColumnWidth(1, 75)
        self.tableWidget.setColumnWidth(2, 175)
        self.tableWidget.setColumnWidth(3, 175)
        self.tableWidget.setObjectName("tableWidget")

        self.btn_load = QtWidgets.QPushButton(self.centralwidget)
        self.btn_load.setGeometry(QtCore.QRect(370, 460, 75, 23))
        self.btn_load.setObjectName("btn_load")
        self.btn_load.clicked.connect(self.loadData)
        self.btn_load.text

        #self.setCentralWidget(self.centralwidget)

        QtCore.QMetaObject.connectSlotsByName(self)


    def loadData(self):
        # connection = sqlite3.connect('D:\ProgrammingD\Python\YandexLicei\QT\warn.db')
        # query = "SELECT * FROM warlist"
        # result = connection.execute(query)
        # self.tableWidget.setRowCount(0)
        # for row_number, row_data in enumerate(result):
        #     self.tableWidget.insertRow(row_number)
        #     for colum_number, data in enumerate(row_data):
        #         self.tableWidget.setItem(row_number, colum_number, QtWidgets.QTableWidgetItem(str(data)))

        #connection.close()

        self.row_count = 1
        #        self.table_index = 0

        #        sqlite_connection = sqlite3.connect("Autosalon.db")
        sqlite_connection = sqlite3.connect("D:\ProgrammingD\Python\YandexLicei\QT\warn.db")  # установить свое
        cursor = sqlite_connection.cursor()

        #        sqlite_select_query = """SELECT * FROM Авто WHERE Название LIKE 'Audi A3%'""" # установить свое
        sqlite_select_query = """SELECT * FROM warlist"""

        cursor.execute(sqlite_select_query)
        records = cursor.fetchall()
        #        print(type(records), records[0][0], records[0][1])

        self.tableWidget.verticalHeader().setDefaultSectionSize(100)  # +++

        for i, row in enumerate(records):
            self.tableWidget.setRowCount(self.row_count)
            self.tableWidget.setItem(i, 0, QtWidgets.QTableWidgetItem(str(row[0])))
            self.tableWidget.setItem(i, 1, QtWidgets.QTableWidgetItem(str(row[1])))

            # +++ vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
            label = QtWidgets.QLabel()
            pix = QPixmap()
            pix.loadFromData(row[2])

            _size = QtCore.QSize(100, 100)
            label.setPixmap(pix.scaled(_size, QtCore.Qt.KeepAspectRatio))

            #            self.tableWidget.setItem(self.table_index, 2, QtWidgets.QTableWidgetItem(str(row[2])))
            self.tableWidget.setCellWidget(i, 2, label)
            self.tableWidget.setItem(i, 3, QtWidgets.QTableWidgetItem(str(row[3])))
            # +++ ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

            #            self.table_index += 1
            self.row_count += 1
        cursor.close()
        sqlite_connection.close()


    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(10, 20, 781, 351))
        self.tableWidget.setRowCount(100)
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setColumnWidth(0, 75)
        self.tableWidget.setColumnWidth(1, 75)
        self.tableWidget.setColumnWidth(2, 175)
        self.tableWidget.setColumnWidth(3, 175)
        self.tableWidget.setObjectName("tableWidget")
        self.btn_load = QtWidgets.QPushButton(self.centralwidget)
        self.btn_load.setGeometry(QtCore.QRect(370, 460, 75, 23))
        self.btn_load.setObjectName("btn_load")

        self.btn_load.clicked.connect(self.loadData)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.btn_load.setText(_translate("MainWindow", "Load"))

'''
def main(self):
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
'''
