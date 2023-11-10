import torch
from facenet_pytorch import MTCNN, InceptionResnetV1
import sqlite3
from PIL import Image
from roboflow import Roboflow
import cv2
import numpy as np
import face_recognition


class FaceDetector:
    def __init__(self, db):
        # con = sqlite3.connect(db)
        # mtcnn = MTCNN()
        # resnet = InceptionResnetV1(pretrained='vggface2').eval()
        rf = Roboflow(api_key="nwjBYhl5xVcVEpDaG187")
        project = rf.workspace().project("face-detection-vswnd")
        self.model = project.version(11).model

    def crop_face(self, face,):
        b = self.model.predict(face, confidence=40, overlap=30).json()
        for prediction in b['predictions']:
            x1 = prediction['x'] - prediction['width'] // 2
            y1 = prediction['y'] - prediction['height'] // 2
            x2 = x1 + prediction['width']
            y2 = y1 + prediction['height']
            coords = (round(x1), round(y1), round(x2), round(y2))
        return coords

    def compare(self, face1, face2, coords1, coords2):
        self.face1 = Image.open(face1)
        self.face2 = Image.open(face2)
        # Получение кодировок лиц
        encoding1 = face_recognition.face_encodings(self.face1)[0]
        encoding2 = face_recognition.face_encodings(self.face2)[0]
        # Вычисление процентной схожести
        similarity = face_recognition.face_distance([encoding1], encoding2)[0] * 100
        return similarity

