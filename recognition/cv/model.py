from .config import CVConfig
from ..model import Model
import os
import pickle
import cv2
from shutil import make_archive, unpack_archive, rmtree


class CVModel(Model):
    def __init__(self):
        super().__init__()
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.confidence, self.precision = CVConfig.CONFIDENCE1, CVConfig.PRECISION1
        self.left, self.right, self.face, self.name = CVConfig.LEFT, CVConfig.RIGHT, None, 'nameless'

    def train(self, x, y):
        self.recognizer.train(x, y)

    def predict(self, img):
        return self.recognizer.predict(img)

    def read(self, face):
        zip_file = face + '/cv.face'
        folder = face + '/cv'
        if not os.path.exists(folder):
            os.makedirs(folder)
        unpack_archive(zip_file, folder, "zip")
        data_file = folder + '/data'
        model_file = folder + '/model'
        with open(data_file, "rb") as f:
            data = pickle.loads(f.read())
        self.recognizer.read(model_file)
        self.confidence, self.precision = data['confidence'], data['precision']
        self.left, self.right, self.face, self.name = data['left'], data['right'], data['face'], data['name']
        rmtree(folder)

    def write(self, face):
        self.face = os.path.split(face)[-1]
        folder = os.path.join(face, 'cv')
        if not os.path.exists(folder):
            os.makedirs(folder)
        data_file = folder + '/data'
        data = {'confidence': self.confidence, 'precision': self.precision, 'left': self.left, 'right': self.right,
                'face': self.face, 'name': self.name}
        with open(data_file, "wb") as f:
            f.write(pickle.dumps(data))
        model_file = folder + '/model'
        self.recognizer.write(model_file)
        zip_file = face + '/cv'
        if os.path.exists(zip_file + '.zip'):
            os.remove(zip_file + '.zip')
        if os.path.exists(zip_file + '.face'):
            os.remove(zip_file + '.face')
        make_archive(zip_file, 'zip', folder)
        os.rename(zip_file + '.zip', zip_file + '.face')
        rmtree(folder)

    def compare(self, frame, boxes, font):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        a, b, trust = 0, 0, []
        for (x, y, w, h) in boxes:
            face = gray[y:y + h, x:x + w]
            name, confidence = self.predict(cv2.resize(face, CVConfig.FACE_SIZE))
            trust.append(confidence)
            if confidence < self.confidence:
                name = 'Known'
                a += 1
                confidence = "  {0} y.e.".format(round(confidence))
            else:
                name = 'Unknown'
                b += 1
                confidence = "  {0} y.e.".format(round(confidence))
            cv2.putText(frame, name, (x + 5, y - 5), font, 1, (255, 255, 255), 2)
            cv2.putText(frame, str(confidence), (x + 5, y + h - 5), font, 1, (255, 0, 0), 1)
        return a, b, trust
