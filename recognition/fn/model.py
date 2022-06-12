from recognition.fn.fr_utils import *
from recognition.fn.inception_blocks_v2 import *
from keras import backend as K
from keras.models import load_model
import pickle
from shutil import make_archive, unpack_archive, rmtree
from ..model import Model


class FaceNetModel(Model):
    @staticmethod
    def triplet_loss(y_true, y_pred, alpha=0.3):
        anchor, positive, negative = y_pred[0], y_pred[1], y_pred[2]
        pos_dist = tf.reduce_sum(tf.square(tf.subtract(anchor, positive)), axis=-1)
        neg_dist = tf.reduce_sum(tf.square(tf.subtract(anchor, negative)), axis=-1)
        basic_loss = tf.add(tf.subtract(pos_dist, neg_dist), alpha)
        loss = tf.reduce_sum(tf.maximum(basic_loss, 0.0))
        return loss

    @staticmethod
    def compile_net():
        K.set_image_data_format('channels_first')
        FaceNetConfig.MODEL = faceRecoModel(input_shape=(3, 96, 96))
        FaceNetConfig.MODEL.compile(optimizer='adam', loss=FaceNetModel.triplet_loss, metrics=['accuracy'])
        load_weights_from_FaceNet(FaceNetConfig.MODEL)
        FaceNetConfig.MODEL.save(FaceNetConfig.MODEL_FOLDER)

    @staticmethod
    def load_net():
        FaceNetConfig.MODEL = load_model(FaceNetConfig.MODEL_FOLDER, custom_objects={'triplet_loss':
                                                                                         FaceNetModel.triplet_loss})

    def __init__(self):
        super().__init__()
        self.x, self.y = [], []
        self.confidence, self.precision = FaceNetConfig.CONFIDENCE, FaceNetConfig.PRECISION
        self.left, self.right, self.face, self.name = FaceNetConfig.LEFT, FaceNetConfig.RIGHT, None, 'nameless'

    def train(self, x, y):
        self.y = y
        self.x = [img_to_encoding(_, FaceNetConfig.MODEL) for _ in x]

    def predict(self, img):
        encoding = img_to_encoding(img, FaceNetConfig.MODEL)
        min_dist, identity, ln = 100, None, len(self.x)
        for i in range(ln):
            dist = np.linalg.norm(self.x[i] - encoding)
            if dist < min_dist:
                min_dist = dist
                identity = self.y[i]
        return identity, min_dist

    def read(self, face):
        zip_file = face + '/fn.face'
        folder = face + '/fn'
        if not os.path.exists(folder):
            os.makedirs(folder)
        unpack_archive(zip_file, folder, "zip")
        data_file = folder + '/data'
        model_file = folder + '/model'
        with open(data_file, "rb") as f:
            data = pickle.loads(f.read())
        self.confidence, self.precision = data['confidence'], data['precision']
        self.left, self.right, self.face, self.name = data['left'], data['right'], data['face'], data['name']
        with open(model_file, "rb") as f:
            data = pickle.loads(f.read())
        self.x, self.y = data['x'], data['y']
        rmtree(folder)

    def write(self, face):
        self.face = os.path.split(face)[-1]
        folder = os.path.join(face, 'fn')
        if not os.path.exists(folder):
            os.makedirs(folder)
        data_file = folder + '/data'
        data = {'confidence': self.confidence, 'precision': self.precision, 'left': self.left, 'right': self.right,
                'face': self.face, 'name': self.name}
        with open(data_file, "wb") as f:
            f.write(pickle.dumps(data))
        model_file = folder + '/model'
        data = {'x': self.x, 'y': self.y}
        with open(model_file, "wb") as f:
            f.write(pickle.dumps(data))
        zip_file = face + '/fn'
        if os.path.exists(zip_file + '.zip'):
            os.remove(zip_file + '.zip')
        if os.path.exists(zip_file + '.face'):
            os.remove(zip_file + '.face')
        make_archive(zip_file, 'zip', folder)
        os.rename(zip_file + '.zip', zip_file + '.face')
        rmtree(folder)

    def compare(self, frame, boxes, font):
        a, b, trust = 0, 0, []
        for (x, y, w, h) in boxes:
            face = frame[y:y + h, x:x + w]
            name, confidence = self.predict(cv2.resize(face, FaceNetConfig.FACE_SIZE))
            trust.append(confidence)
            if confidence < self.confidence:
                name = 'Known'
                a += 1
                confidence = "  {0} y.e.".format(round(confidence))
            else:
                name = 'Unknown'
                b += 1
                confidence = "  {0} y.e.".format(round(confidence))
            cv2.putText(frame, name, (x + 5, y - 5), font, 1, (255, 255, 255), 2)
            cv2.putText(frame, str(confidence), (x + 5, y + h - 5), font, 1, (255, 0, 0), 1)
        return a, b, trust
