from .cv import CVModel
import cv2
from .detector import Detector
from glob import glob
from os import path, makedirs
from shutil import rmtree
from .config import Config
from .utils import get_font
from datetime import datetime


class Logger:
    def __init__(self):
        self.text, self.p, self.m, self.trust1, self.trust2, self.emp, self.start = [], 0, 0, [], [], [], datetime.now()

    def log(self, p, m, trust, name1, name2, file):
        if name1 == name2:
            if m:
                self.text.append('Ложно «чужой»: {}; {}'.format(file, trust))
                self.m += m
            self.trust1.extend(trust)
        if name1 != name2:
            if p:
                self.text.append('Ложно «свой»: модель: {}, тест: {}; {}'.format(name1, file, trust))
                self.p += p
            self.trust2.extend(trust)

    def empty(self, name):
        self.emp.append(name)

    def save(self, file1, file2):
        end = datetime.now()
        with open(file1, 'w', encoding='UTF-8') as f:
            f.write('Пустые данные ({}): {}\n'.format(len(self.emp), self.emp))
            f.write('Время выполнения: {}\n'.format(str(end - self.start).split('.')[0]))
            f.write('Само проверки ({}):\n'.format(len(self.trust1)))
            f.write('{}\n'.format(sorted(self.trust1)))
            f.write('Обычные проверки ({}):\n'.format(len(self.trust2)))
            f.write('{}\n'.format(sorted(self.trust2)))
        with open(file2, 'w', encoding='UTF-8') as f:
            f.write('Ошибочность: {}\n'.format((self.m + 10 * self.p) / (len(self.trust1) + len(self.trust2))))
            f.write('Количество ложно «чужих»: {}\n'.format(self.m))
            f.write('Количество ложно «своих»: {}\n'.format(self.p))
            f.write('\n'.join(self.text) + '\n')


def test():
    detector, font, logger = Detector(), get_font(), Logger()
    names = [_.split('\\')[-1] for _ in glob(Config.DATASET + '/*')]
    tmp = Config.DATASET + '/test'
    if not path.exists(tmp):
        makedirs(tmp)
    for name1 in names:
        print(name1)
        f1 = Config.DATASET + '/' + name1
        model = CVModel()
        data = detector.get_data(f1, tmp)
        if len(data[0]) == 0:
            logger.empty(name1)
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
    logger.save('log1.txt', 'log2.txt')
