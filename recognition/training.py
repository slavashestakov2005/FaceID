from imutils import paths
import face_recognition
import pickle
import cv2
from PIL import Image
import numpy as np
from .recognition import get_detector_default_cv, get_recognizer_cv, detect_faces_numpy_cv


def train_fr(folder):
    images = list(paths.list_images(folder))
    known_encodings = []
    for (i, imagePath) in enumerate(images):
        image = cv2.imread(imagePath)
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        boxes = face_recognition.face_locations(rgb, model='hog')
        encodings = face_recognition.face_encodings(rgb, boxes)
        for encoding in encodings:
            known_encodings.append(encoding)
    data = {"encodings": known_encodings}
    f = open(folder + '.face', "wb")
    f.write(pickle.dumps(data))
    f.close()
    return folder + '.face'


def train_cv(folder):
    detector, recognizer = get_detector_default_cv(), get_recognizer_cv()
    images = list(paths.list_images(folder))
    data1, data2 = [], []
    for (i, imagePath) in enumerate(images):
        image = Image.open(imagePath).convert('L')
        img_numpy = np.array(image, 'uint8')
        faces = detect_faces_numpy_cv(detector, img_numpy)
        for (x, y, w, h) in faces:
            data1.append(img_numpy[y:y + h, x:x + w])
            data2.append(0)
    recognizer.train(data1, np.array(data2))
    recognizer.write(folder + '.face')
    return folder + '.face'
