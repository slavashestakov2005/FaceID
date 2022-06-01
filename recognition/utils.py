import cv2
from imutils import paths
from glob import glob
from random import shuffle
from shutil import copyfile
from os import makedirs
from .config import Config


def get_font():
    return cv2.FONT_HERSHEY_SIMPLEX


def chose_images(folder):
    images = list(paths.list_images(folder))
    length, new_images = len(images), []
    if length <= Config.IMAGES_COUNT:
        return images
    step = length // Config.IMAGES_COUNT
    i = (length - step * Config.IMAGES_COUNT) // 2
    while i < length and len(new_images) < Config.IMAGES_COUNT:
        new_images.append(images[i])
        i += step
    return new_images


def split_data(folder, test_size=0.15, chose_count=-1):
    files = list(glob(folder + '/*.png'))
    shuffle(files)
    if chose_count != -1:
        fd = folder + '/' + str(chose_count)
        makedirs(fd)
        for i in range(chose_count):
            copyfile(files[i], fd + '/{}.png'.format(i))
        return
    test = int(test_size * len(files))
    for i in range(test):
        copyfile(files[i], folder + '/test/{}.png'.format(i))
    for i in range(test, len(files)):
        copyfile(files[i], folder + '/train/{}.png'.format(i - test))
