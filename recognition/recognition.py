# import face_recognition
import cv2
from .config import Config


def get_detector_alt2_cv():
    return cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_alt2.xml')


def get_detector_default_cv():
    return cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')


def detect_faces_cv(detector, image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return detector.detectMultiScale(gray, **Config.DETECTOR_KWARGS, flags=cv2.CASCADE_SCALE_IMAGE)


def detect_faces_numpy_cv(detector, img_numpy):
    return detector.detectMultiScale(img_numpy, **Config.DETECTOR_KWARGS, flags=cv2.CASCADE_SCALE_IMAGE)


# def detect_faces_fr(image):
#     rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#     return face_recognition.face_locations(rgb, model='hog')


def compare_faces_cv(frame, boxes, recognizer, font):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    a, b, trust = 0, 0, []
    for (x, y, w, h) in boxes:
        face = gray[y:y + h, x:x + w]
        name, confidence = recognizer.predict(cv2.resize(face, Config.FACE_SIZE))
        trust.append(confidence)
        if confidence < recognizer.confidence:
            name = 'Known'
            a += 1
            confidence = "  {0} y.e.".format(round(confidence))
        else:
            name = 'Unknown'
            b += 1
            confidence = "  {0} y.e.".format(round(confidence))
        # print(name, confidence)
        cv2.putText(frame, name, (x + 5, y - 5), font, 1, (255, 255, 255), 2)
        cv2.putText(frame, str(confidence), (x + 5, y + h - 5), font, 1, (255, 0, 0), 1)
    return a, b, trust


# def compare_faces_fr(image, boxes, face):
#     rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#     faces = face_recognition.face_encodings(rgb, boxes)
#     a, b = 0, 0
#     for encoding in faces:
#         matches = face_recognition.compare_faces(face["encodings"], encoding)
#         if any(matches):
#             a += 1
#         else:
#             b += 1
#     return a, b


def get_recognizer_cv():
    return cv2.face.LBPHFaceRecognizer_create()


def get_font():
    return cv2.FONT_HERSHEY_SIMPLEX
