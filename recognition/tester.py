from .fn import FaceNetModel
import cv2
from .detector import Detector
from glob import glob
from os import path, makedirs
from shutil import rmtree
from .config import Config
from .utils import get_font


class Logger:
    def __init__(self):
        self.text, self.p, self.m, self.cnt = [], 0, 0, 0

    def log(self, p, m, trust, name1, name2, file):
        if name1 == name2 and m:
            self.text.append('Ложно «чужой»: {}; {}'.format(file, trust))
            self.m += m
        if name1 != name2 and p:
            self.text.append('Ложно «свой»: модель: {}, тест: {}; {}'.format(name1, file, trust))
            self.p += p
        self.cnt += 1

    def save(self, file):
        with open(file, 'w', encoding='UTF-8') as f:
            f.write('Ошибочность: {}\n'.format((self.m + 10 * self.p) / self.cnt))
            f.write('Количество ложно «чужих»: {}\n'.format(self.m))
            f.write('Количество ложно «своих»: {}\n'.format(self.p))
            f.write('\n'.join(self.text) + '\n')


def test():
    detector, font, logger = Detector(), get_font(), Logger()
    names = [_.split('\\')[-1] for _ in glob(Config.DATASET + '/*')]
    tmp = Config.DATASET + '/test'
    Config.MIN_FACE_SIZE = (30, 30)
    if not path.exists(tmp):
        makedirs(tmp)
    for name1 in names:
        print(name1)
        f1 = Config.DATASET + '/' + name1
        model = FaceNetModel()
        data = detector.get_data(f1, tmp, False)
        if len(data[0]) == 0:
            print("Empty data: " + name1)
            continue
        model.train(*data)
        for name2 in names:
            f2 = Config.DATASET + '/' + name2
            for face in glob(f2 + '/*.jpg'):
                frame = cv2.imread(face)
                boxes = detector.detect_image(frame)
                logger.log(*model.compare(frame, boxes, font), name1, name2, face[len(f2) + 1:])
    if path.exists(tmp):
        rmtree(tmp)
    logger.save('log.txt')
