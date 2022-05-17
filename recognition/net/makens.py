import glob
from recognition.net.fr_utils import *
from recognition.net.inception_blocks_v2 import *
from keras import backend as K
from keras.models import load_model
from recognition import Config


def triplet_loss(y_true, y_pred, alpha = 0.3):
    anchor, positive, negative = y_pred[0], y_pred[1], y_pred[2]
    pos_dist = tf.reduce_sum(tf.square(tf.subtract(anchor, positive)), axis=-1)
    neg_dist = tf.reduce_sum(tf.square(tf.subtract(anchor, negative)), axis=-1)
    basic_loss = tf.add(tf.subtract(pos_dist, neg_dist), alpha)
    loss = tf.reduce_sum(tf.maximum(basic_loss, 0.0))
    return loss


def compile_net():
    K.set_image_data_format('channels_first')
    Config.model = faceRecoModel(input_shape=(3, 96, 96))
    Config.model.compile(optimizer='adam', loss=triplet_loss, metrics=['accuracy'])
    load_weights_from_FaceNet(Config.model)
    Config.model.save(Config.MODEL_FOLDER)


def load_net():
    Config.model = load_model(Config.MODEL_FOLDER, custom_objects={'triplet_loss': triplet_loss})


def prepare_database(path):
    database = {}
    for file in glob.glob(path + "/*"):
        identity = os.path.splitext(os.path.basename(file))[0]
        database[identity] = img_path_to_encoding(file, Config.model)
    return database
