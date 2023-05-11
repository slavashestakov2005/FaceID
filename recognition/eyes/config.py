import cv2


class EyeConfig:
    DETECTOR_ARGS = {'scaleFactor': 1.1, 'minNeighbors': 5, 'minSize': (30, 30), 'flags': cv2.CASCADE_SCALE_IMAGE}
    IMAGE_GENERATOR_ARGS = {'rescale': 1. / 255, 'shear_range': 0.2, 'horizontal_flip': True}
    IMG_SIZE = 24
    DATASETS_INFO = {'target_size': (IMG_SIZE, IMG_SIZE), 'color_mode': "grayscale", 'batch_size': 32,
                     'class_mode': "binary", 'shuffle': True, 'seed': 42}
    FOLDER = 'recognition/eyes/'
    MAX_FRAMES = 3
