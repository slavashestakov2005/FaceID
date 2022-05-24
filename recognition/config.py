class Config:
    CV_CONFIDENCE1 = 60
    CV_CONFIDENCE2 = 55
    CV_PRECISION1 = 80
    CV_PRECISION2 = 65
    CV_LEFT = 20
    CV_RIGHT = 140
    PADDING = 5
    MODEL_FOLDER = 'server/data/model'
    IMAGES_COUNT = 250
    FACE_SIZE = (300, 300)
    MIN_FACE_SIZE = (150, 150)
    DETECTOR_KWARGS = {'scaleFactor': 1.2, 'minNeighbors': 5, 'minSize': MIN_FACE_SIZE}
    PLOT_TIME = 5
