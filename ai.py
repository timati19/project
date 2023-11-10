class FaceDetector:
    def __init__(self):
        from roboflow import Roboflow
        from facenet_pytorch import MTCNN, InceptionResnetV1
        rf = Roboflow(api_key="nwjBYhl5xVcVEpDaG187")
        project = rf.workspace().project("face-detection-vswnd")
        self.model = project.version(11).model
        self.mtcnn = MTCNN()
        self.resnet = InceptionResnetV1(pretrained='vggface2').eval()

    def crop_face(self, face):
        b = self.model.predict(face, confidence=40, overlap=30).json()
        for prediction in b['predictions']:
            x1 = prediction['x'] - prediction['width'] // 2
            y1 = prediction['y'] - prediction['height'] // 2
            x2 = x1 + prediction['width']
            y2 = y1 + prediction['height']
            coords = (round(x1), round(y1), round(x2), round(y2))
        return coords

    def compare(self, face1, face2, coords):
        from PIL import Image
        import torch
        self.face1 = face1
        self.face2 = Image.open(face2).crop(coords)
        known_face = self.mtcnn(self.face1)
        unknown_face = self.mtcnn(self.face2)
        known_embedding = self.resnet(known_face.unsqueeze(0))
        unknown_embedding = self.resnet(unknown_face.unsqueeze(0))
        # Вычисление процентной схожести
        distance = torch.nn.functional.pairwise_distance(known_embedding, unknown_embedding)
        similarity = (1 - distance.item()) * 100

        return similarity
