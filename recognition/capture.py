from .detector import Detector
from .config import Config
import cv2
from time import time


def capture_data(path, video=None):
    cv2.namedWindow('preview')
    video_capture = cv2.VideoCapture(0)
    detector = Detector()
    if video:
        frame_size = (int(video_capture.get(3)), int(video_capture.get(4)))
        output = cv2.VideoWriter(video, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 20, frame_size)
    cnt, start = 0, time()
    while video_capture.isOpened():
        ret, frame = video_capture.read()
        boxes = detector.detect_image(frame)
        if video:
            output.write(frame)
        if len(boxes):
            for (x, y, w, h) in boxes:
                x1 = x - Config.PADDING
                y1 = y - Config.PADDING
                x2 = x + w + Config.PADDING
                y2 = y + h + Config.PADDING
                cv2.imwrite(path + '/{}.jpg'.format(cnt), cv2.resize(frame[y1:y2, x1:x2], Config.FACE_SIZE))
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                cnt += 1
        cv2.imshow('preview', frame)
        now = time()
        if cv2.waitKey(1) == 27 or cv2.getWindowProperty('preview', 0) == -1 or now - start > Config.CAPTURE_TIME:
            break
        print('Прошло секунд: {}'.format(int(now - start)), end='\r')
    video_capture.release()
    cv2.destroyAllWindows()
    if video:
        output.release()
    return cnt
