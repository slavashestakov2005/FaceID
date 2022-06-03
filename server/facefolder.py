from os import path, makedirs
from shutil import rmtree
from time import time
from .config import Config


class FaceFolder:
    def __init__(self, name=None):
        self.url = (str(int(time() * 1000)) if name is None else name)
        self.folder = path.join(Config.DATA_FOLDER, self.url)

    def face(self):
        return self.url

    def dir(self):
        return self.folder

    def image(self):
        return path.join(self.folder, 'image')

    def video(self):
        return path.join(self.folder, 'video')

    def temp(self):
        return path.join(self.folder, 'temp')

    def temp2(self):
        return path.join(self.folder, 'temp2')

    def images_archive(self):
        return path.join(self.folder, 'images')

    def cv_model(self):
        return path.join(self.folder, 'cv.face')

    def create(self, remove_old=True):
        if path.exists(self.folder) and remove_old:
            rmtree(self.folder)
        video_directory = self.video()
        image_directory = self.image()
        temp_directory = self.temp()
        temp2_directory = self.temp2()
        if not path.exists(self.folder):
            makedirs(self.folder)
        if not path.exists(video_directory):
            makedirs(video_directory)
        if not path.exists(image_directory):
            makedirs(image_directory)
        if not path.exists(temp_directory):
            makedirs(temp_directory)
        if not path.exists(temp2_directory):
            makedirs(temp2_directory)

    def clear(self):
        dirs = [self.temp(), self.temp2()]
        for directory in dirs:
            if path.exists(directory):
                rmtree(directory)
            makedirs(directory)
