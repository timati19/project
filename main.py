import sys

import PIL.Image
from PyQt5 import QtCore, QtSql
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication, QFileDialog, QLabel, QVBoxLayout, QLineEdit, QTableView
from ai import FaceDetector
from database import FaceTable


class Detector(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(0, 0, 600, 600)
        self.setWindowTitle('Детектор номеров')
        self.btn = QPushButton('Выбрать фото', self)
        self.btn.move(20, 500)
        self.btn.clicked.connect(self.load_image)
        self.pic = QLabel('Изображение:', self)
        self.pic.move(10, 30)
        self.pic.setMaximumSize(200, 200)
        self.pic.show()
        self.opp_img = QLabel(self)
        self.opp_img.move(250, 30)
        self.open_btn = QPushButton('Просмотр БД', self)
        self.open_btn.clicked.connect(self.db)
        self.open_btn.move(320, 500)
        self.scan_but = QPushButton('Скан', self)
        self.scan_but.move(170, 500)
        self.scan_but.clicked.connect(self.scan)
        self.database = FaceTable('faces.db')
        self.detector = FaceDetector()
        self.scan_but.setEnabled(False)
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.pic)

    def load_image(self):
        file_name = QFileDialog.getOpenFileName()
        print(file_name)
        self.img1 = QPixmap(file_name[0])
        self.img = PIL.Image.open(file_name[0])
        coords = self.detector.crop_face(file_name[0])
        self.img = self.img.crop(coords)
        self.scan_but.setEnabled(True)

    def db(self):
        self.database_win = Database_window()
        self.database_win.show()

    def scan(self):
        database_faces = self.database.get_faces()
        for i in database_faces:
            result = self.detector.compare(self.img, i[1], self.detector.crop_face(i[1]))
            print(result)
            if result > 10:
                self.sim = result
                self.pers = i
                break
        print(str(self.pers[2]))
        self.opp_img.setText(self.pers[2])
        self.opp_img.adjustSize()


class Database_window(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(0, 0, 600, 600)
        self.setWindowTitle('База данных')
        self.database = QtSql.QSqlDatabase('faces.db')
        self.database.open()
        self.db = QtSql.QSqlDatabase.addDatabase('faces.db')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Detector()
    ex.show()
    sys.exit(app.exec())

