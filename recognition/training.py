from imutils import paths
import face_recognition
import pickle
import cv2
from PIL import Image
import numpy as np
from .recognition import get_detector_default_cv, detect_faces_numpy_cv, detect_faces_cv
from .cvmodel import CVModel
from .config import Config
from glob import glob


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


def train_cv(folder, folder_to):
    detector, recognizer = get_detector_default_cv(), CVModel()
    images = list(paths.list_images(folder))
    data1, data2 = [], []
    for (i, imagePath) in enumerate(images):
        image = Image.open(imagePath).convert('L')
        img_numpy = np.array(image, 'uint8')
        faces = detect_faces_numpy_cv(detector, img_numpy)
        for (x, y, w, h) in faces:
            face = img_numpy[y:y + h, x:x + w]
            cv2.imwrite(folder_to + '/' + str(len(data2)) + '.png', face)
            data1.append(face)
            data2.append(0)
    recognizer.train(data1, np.array(data2))
    recognizer.write(folder)


def parse_image_cv(folder_from, folder_to):
    detector = get_detector_default_cv()
    i, p = 0, Config.PADDING
    for file in glob(folder_from + '/*.*'):
        image = cv2.imread(file)
        faces = detect_faces_cv(detector, image)
        for (x, y, w, h) in faces:
            face = image[y - p:y + h + p, x - p:x + w + p]
            cv2.imwrite(folder_to + '/' + str(i) + '.png', face)
            i += 1


def parse_video_cv(folder_from, folder_to):
    detector = get_detector_default_cv()
    i, p = 0, Config.PADDING
    for file in glob(folder_from + '/*.*'):
        stream = cv2.VideoCapture(file)
        while stream.isOpened():
            ret, image = stream.read()
            # image = cv2.rotate(image, cv2.cv2.ROTATE_90_CLOCKWISE)
            if not ret:
                break
            faces = detect_faces_cv(detector, image)
            for (x, y, w, h) in faces:
                try:
                    face = image[y - p:y + h + p, x - p:x + w + p]
                    cv2.imwrite(folder_to + '/' + str(i) + '.png', face)
                    i += 1
                except Exception as ex:  # empty image
                    pass
