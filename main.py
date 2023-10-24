import sys
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton
from PIL import Image
import torch
from facenet_pytorch import MTCNN, InceptionResnetV1

class Face_control(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(600, 600, 600, 600)
        self.image_but1 = QPushButton()
        self.setWindowTitle('Отображение картинки')
        self.image = QLabel(self)

    def Face_control(self):
        self.im.putalpha(self.alpha.value())
        self.im.save('new.png')
        self.pixmap = QPixmap('new.png')
        self.image.setPixmap(self.pixmap)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Face_control()
    ex.show()
    sys.exit(app.exec())


mtcnn = MTCNN()
resnet = InceptionResnetV1(pretrained='vggface2').eval()


def compare(known_face, unknown_face):
    known_image = Image.open(known_face)
    unknown_image = Image.open(unknown_face)
    known_face = mtcnn(known_image)
    unknown_face = mtcnn(unknown_image)
    known_embedding = resnet(known_face.unsqueeze(0))
    unknown_embedding = resnet(unknown_face.unsqueeze(0))
    distance = torch.nn.functional.pairwise_distance(known_embedding, unknown_embedding)
    similarity_percentage = (1 - distance.item()) * 100
    if similarity_percentage >= 40:
        print(f'Это один и тот же человек! {round(similarity_percentage, 1)} %!')
    else:
        print(f'😭{round(similarity_percentage, 1)} %(((')

compare('known_face.jpg', 'unknown_face.jpg')