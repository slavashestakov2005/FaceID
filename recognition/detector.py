from .config import Config
from .utils import chose_images
import cv2
from glob import glob
import numpy as np


class Detector:
    def __init__(self, default=True):
        path = cv2.data.haarcascades + 'haarcascade_frontalface_{}.xml'.format('default' if default else 'alt2')
        self.detector = cv2.CascadeClassifier(path)

    def detect_image(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return self.detector.detectMultiScale(gray, **Config.DETECTOR_KWARGS)

    def detect_numpy(self, img_numpy):
        return self.detector.detectMultiScale(img_numpy, **Config.DETECTOR_KWARGS)

    def parse_images(self, folder_from, folder_to, start=0):
        i, p = start, Config.PADDING
        for file in glob(folder_from + '/*.*'):
            image = cv2.imread(file)
            faces = self.detect_image(image)
            for (x, y, w, h) in faces:
                try:
                    face = image[y - p:y + h + p, x - p:x + w + p]
                    cv2.imwrite(folder_to + '/' + str(i) + '.png', face)
                    i += 1
                except Exception as ex:  # empty image
                    pass
        return i

    def parse_videos(self, folder_from, folder_to, start=0, angle=0):
        i, p = start, Config.PADDING
        for file in glob(folder_from + '/*.*'):
            stream = cv2.VideoCapture(file)
            while stream.isOpened():
                ret, image = stream.read()
                if angle:
                    image = cv2.rotate(image, Config.ANGLE[angle])
                if not ret:
                    break
                faces = self.detect_image(image)
                for (x, y, w, h) in faces:
                    try:
                        face = image[y - p:y + h + p, x - p:x + w + p]
                        cv2.imwrite(folder_to + '/' + str(i) + '.png', face)
                        i += 1
                    except Exception as ex:  # empty image
                        pass
        return i

    def get_data(self, folder_from, folder_to, gray=True):
        images = chose_images(folder_from)
        data1, data2 = [], []
        for (i, imagePath) in enumerate(images):
            image = cv2.imread(imagePath)
            faces = self.detect_image(image)
            if gray:
                image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            for (x, y, w, h) in faces:
                face = image[y:y + h, x:x + w]
                face = cv2.resize(face, Config.FACE_SIZE)
                cv2.imwrite(folder_to + '/' + str(len(data2)) + '.png', face)
                data1.append(face)
                data2.append(0)
        return data1, np.array(data2)
