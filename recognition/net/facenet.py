import pickle
from .fr_utils import *
from .inception_blocks_v2 import *
from .makens import prepare_database
from recognition.config import Config
from recognition.detector import Detector


def process_frame(frame, detector, database):
    faces = detector.detect_image(frame)
    identities = []
    for (x, y, w, h) in faces:
        x1 = x - Config.PADDING
        y1 = y - Config.PADDING
        x2 = x + w + Config.PADDING
        y2 = y + h + Config.PADDING
        frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
        identity = find_identity(frame, database, x1, y1, x2, y2, Config.model)
        if identity is not None:
            identities.append(identity)
    return frame


def find_identity(frame, database, x1, y1, x2, y2, FRmodel):
    height, width, channels = frame.shape
    part_image = frame[max(0, y1):min(height, y2), max(0, x1):min(width, x2)]
    return who_is_it(part_image, database, FRmodel)


def who_is_it(image, database, model):
    encoding = img_to_encoding(image, model)
    min_dist = 100
    identity = None
    for (name, db_enc) in database.items():
        dist = np.linalg.norm(db_enc - encoding)
        if dist < min_dist:
            min_dist = dist
            identity = name
    print(identity, min_dist, end="")
    if min_dist > 0.52:
        print(' - Bad')
        return None
    else:
        print(' - Good')
        return str(identity)


def train_net(folder):
    data = prepare_database(folder)
    f = open(folder + '.face', "wb")
    f.write(pickle.dumps(data))
    f.close()
    return folder + '.face'


def capture_stream_net(face_path):
    database = pickle.loads(open(face_path, "rb").read())
    detector = Detector()

    cv2.namedWindow("preview")
    video_capture = cv2.VideoCapture(0)
    while True:
        ret, frame = video_capture.read()
        img = process_frame(frame, detector, database)
        key = cv2.waitKey(1)
        cv2.imshow("preview", img)
        if key == 27:
            break
    cv2.destroyWindow("preview")
