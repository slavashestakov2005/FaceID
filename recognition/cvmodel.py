from .recognition import get_recognizer_cv
from .config import Config
import os
import pickle
from shutil import make_archive, unpack_archive, rmtree


class CVModel:
    def __init__(self):
        self.recognizer = get_recognizer_cv()
        self.confidence, self.precision = Config.CV_CONFIDENCE1, Config.CV_PRECISION1
        self.left, self.right = Config.CV_LEFT, Config.CV_RIGHT

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
        self.left, self.right = data['left'], data['right']
        rmtree(folder)

    def write(self, face):
        folder = os.path.join(face, 'cv')
        if not os.path.exists(folder):
            os.makedirs(folder)
        data_file = folder + '/data'
        data = {'confidence': self.confidence, 'precision': self.precision, 'left': self.left, 'right': self.right}
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
