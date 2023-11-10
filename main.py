import sys

import PIL.Image
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication, QFileDialog, QLabel, QVBoxLayout, QLineEdit, QTableView
import torch
from facenet_pytorch import MTCNN, InceptionResnetV1
from PIL import Image
import sqlite3
from ai import FaceDetector


class Detector(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    @classmethod
    def b(self):
        self.ai = FaceDetector

    def initUI(self):
        self.setGeometry(0, 0, 600, 600)
        self.setWindowTitle('Детектор номеров')

        self.btn = QPushButton('Выбрать фото', self)
        self.btn.move(20, 500)
        self.btn.clicked.connect(self.load_image)
        self.label1 = QLabel('Изображение:', self)
        self.label1.move(10, 30)
        self.label1.hide()
        self.layout1 = QVBoxLayout()
        self.layout1.addStretch()
        self.open_btn = QPushButton('Выбрать БД', self)
        self.open_btn.move(320, 500)
        #self.open_btn.clicked.connect(self.openWin)

    def load_image(self):
        file_name = QFileDialog.getOpenFileName()
        if file_name:
            self.label3 = QLabel(self)
            self.img = QPixmap(file_name)
            self.label3.setPixmap(self.img)
            self.label3.show()






if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Detector()
    ex.show()
    sys.exit(app.exec())

mtcnn = MTCNN()
resnet = InceptionResnetV1(pretrained='vggface2').eval()
