import cv2
from PIL import Image
from .config import EyeConfig
from .model import predict, load_model


class Eyes:
    def __init__(self):
        self.face_detector = cv2.CascadeClassifier(EyeConfig.FOLDER + 'haarcascade_frontalface_alt.xml')
        self.open_eyes_detector = cv2.CascadeClassifier(EyeConfig.FOLDER + 'haarcascade_eye_tree_eyeglasses.xml')
        self.left_eye_detector = cv2.CascadeClassifier(EyeConfig.FOLDER + 'haarcascade_lefteye_2splits.xml')
        self.right_eye_detector = cv2.CascadeClassifier(EyeConfig.FOLDER + 'haarcascade_righteye_2splits.xml')
        self.maxFrames = EyeConfig.MAX_FRAMES
        self.eyes = ''
        self.model = load_model()

    def start(self):
        self.eyes = ''

    def state(self):
        print(self.eyes)
        history = '1' + ''.join('0' if c == '0' else '1' for c in self.eyes) + '1'
        for i in range(self.maxFrames):
            pattern = '1' + '0' * (i + 1) + '1'
            if pattern in history:
                return True
        return False

    def count_open_eyes(self, frame, x, y, w, h) -> int:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray_face = gray[y:y + h, x:x + w]
        open_eyes_glasses = self.open_eyes_detector.detectMultiScale(gray_face, **EyeConfig.DETECTOR_ARGS)
        if len(open_eyes_glasses) == 2:
            self.eyes += '2'
        else:
            left_face = frame[y:y + h, x + int(w / 2):x + w]
            left_face_gray = gray[y:y + h, x + int(w / 2):x + w]

            right_face = frame[y:y + h, x:x + int(w / 2)]
            right_face_gray = gray[y:y + h, x:x + int(w / 2)]

            left_eye = self.left_eye_detector.detectMultiScale(left_face_gray, **EyeConfig.DETECTOR_ARGS)
            right_eye = self.right_eye_detector.detectMultiScale(right_face_gray, **EyeConfig.DETECTOR_ARGS)

            eye_status = 0

            for (ex, ey, ew, eh) in right_eye:
                pred = predict(right_face[ey:ey + eh, ex:ex + ew], self.model)
                if pred == 'open':
                    eye_status += 1
            for (ex, ey, ew, eh) in left_eye:
                pred = predict(left_face[ey:ey + eh, ex:ex + ew], self.model)
                if pred == 'open':
                    eye_status += 1
            self.eyes += str(eye_status)
        return int(self.eyes[-1])
