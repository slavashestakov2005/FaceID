import cv2


class Config:
    PADDING = 10
    IMAGES_COUNT = 250
    FACE_SIZE = (300, 300)
    MIN_FACE_SIZE = (150, 150)
    DETECTOR_KWARGS = {'scaleFactor': 1.2, 'minNeighbors': 5, 'minSize': MIN_FACE_SIZE, 'flags': cv2.CASCADE_SCALE_IMAGE}
    ANGLE = {90: cv2.cv2.ROTATE_90_COUNTERCLOCKWISE, 180: cv2.cv2.ROTATE_180, -90: cv2.cv2.ROTATE_90_CLOCKWISE}
    PLOT_TIME = 5
    CAPTURE_TIME = 30
    PLAY_TIME = 60
    DATASET = 'dataset'
