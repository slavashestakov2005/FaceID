from .recognition import *
from telegram import send_message
import cv2
import pickle


def capture_stream_fr(face_path):
    face = pickle.loads(open(face_path, "rb").read())
    video_capture = cv2.VideoCapture(0)
    while True:
        ret, frame = video_capture.read()
        boxes = detect_faces_fr(frame)
        for (t, r, b, l) in boxes:
            cv2.rectangle(frame, (l, t), (r, b), (0, 255, 0), 2)
        cv2.imshow("Frame", frame)
        a, b = compare_faces_fr(frame, boxes, face)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        if a:
            send_message('«Своих»: {}, «чужих»: {}'.format(a, b))
    video_capture.release()
    cv2.destroyAllWindows()


def capture_stream_cv(face_path):
    recognizer = get_recognizer_cv()
    recognizer.read(face_path)
    detector = get_detector_default_cv()
    font = get_font()
    video_capture = cv2.VideoCapture(0)
    while True:
        ret, frame = video_capture.read()
        boxes = detect_faces_cv(detector, frame)
        for (x, y, w, h) in boxes:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        a, b = compare_faces_cv(frame, boxes, recognizer, font)
        cv2.imshow("Frame", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        if a:
            send_message('«Своих»: {}, «чужих»: {}'.format(a, b))
    video_capture.release()
    cv2.destroyAllWindows()
