from .cv import CVModel
from .trustmetric import TrustMetric
from .detector import Detector
from .utils import get_font
from time import time
from telegram import send_message
import cv2
# import pickle
from glob import glob


# def capture_stream_fr(face_path):
#     face = pickle.loads(open(face_path, "rb").read())
#     video_capture = cv2.VideoCapture(0)
#     while True:
#         ret, frame = video_capture.read()
#         boxes = detect_faces_fr(frame)
#         for (t, r, b, l) in boxes:
#             cv2.rectangle(frame, (l, t), (r, b), (0, 255, 0), 2)
#         cv2.imshow("Frame", frame)
#         a, b = compare_faces_fr(frame, boxes, face)
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
#         if a:
#             send_message('«Своих»: {}, «чужих»: {}'.format(a, b))
#     video_capture.release()
#     cv2.destroyAllWindows()


def capture_stream_cv(face_path, video=None, result=None):
    recognizer, trust_metric, detector, font = CVModel(), TrustMetric(), Detector(), get_font()
    recognizer.read(face_path)
    trust_metric.load_from_model(recognizer)
    video_capture = cv2.VideoCapture(0)
    if video:
        frame_size = (int(video_capture.get(3)), int(video_capture.get(4)))
        output = cv2.VideoWriter(video, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 20, frame_size)
    trust_metric.open_window()
    while True:
        ret, frame = video_capture.read()
        if video:
            output.write(frame)
        tim = time()
        boxes = detector.detect_image(frame)
        a, b, trust = recognizer.compare(frame, boxes, font)
        for i in range(len(boxes)):
            x, y, w, h = boxes[i]
            color = (0, 255, 0)
            if trust[i] > trust_metric.confidence:
                color = (0, 0, 255)
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
        cv2.imshow("Frame", frame)
        if len(trust):
            trust_metric.append(trust[0], tim)
        if cv2.waitKey(1) == 27 or cv2.getWindowProperty('Frame', 0) == -1 or trust_metric.is_closed_plot:
            break
        trust_metric.show()
        # if a:
        #     send_message('«Своих»: {}, «чужих»: {}'.format(a, b))
    video_capture.release()
    cv2.destroyAllWindows()
    if video:
        output.release()
    trust_metric.close_plot()
    answer = trust_metric.get_result()
    trust_metric.show_hist(result)
    send_message(trust_metric.get_message())
    trust_metric.save_to_model(recognizer)
    recognizer.write(face_path)
    return answer


def capture_stream_from_image_folder_cv(face_path, folder):
    recognizer, trust_metric, detector, font = CVModel(), TrustMetric(), Detector(), get_font()
    recognizer.read(face_path)
    trust_metric.load_from_model(recognizer)
    for file in glob(folder + '/*.*'):
        frame = cv2.imread(file)
        tim = time()
        boxes = detector.detect_image(frame)
        for (x, y, w, h) in boxes:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        a, b, trust = recognizer.compare(frame, boxes, font)
        cv2.imshow("Frame", frame)
        if len(trust):
            trust_metric.append(trust[0], tim)
        trust_metric.show()
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        # if a:
        #     send_message('«Своих»: {}, «чужих»: {}'.format(a, b))
    cv2.destroyAllWindows()
    trust_metric.show_hist()
    send_message(trust_metric.get_message())
    trust_metric.save_to_model(recognizer)
    recognizer.write(face_path)
