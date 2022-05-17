from .recognition import *


def capture_data(path):
    cv2.namedWindow("preview")
    video_capture = cv2.VideoCapture(0)
    detector = get_detector_default_cv()
    step, cnt = 0, 0
    while video_capture.isOpened():
        ret, frame = video_capture.read()
        if step % 10 == 9:
            faces = detect_faces_cv(detector, frame)
            if len(faces):
                for (x, y, w, h) in faces:
                    x1 = x - Config.PADDING
                    y1 = y - Config.PADDING
                    x2 = x + w + Config.PADDING
                    y2 = y + h + Config.PADDING
                    cv2.imwrite(path + '/{}.jpg'.format(cnt), frame[y1:y2, x1:x2])
                    cnt += 1
        key = cv2.waitKey(1)
        cv2.imshow("preview", frame)
        if key == 27:
            break
        step += 1
    cv2.destroyWindow("preview")
