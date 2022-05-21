from recognition.videostream import capture_stream_cv, capture_stream_from_image_folder_cv
from glob import glob
from random import shuffle
from shutil import copyfile


def split_data(folder, test_size=0.15):
    files = list(glob(folder + '/*.png'))
    shuffle(files)
    test = int(test_size * len(files))
    for i in range(test):
        copyfile(files[i], folder + '/test/{}.png'.format(i))
    for i in range(test, len(files)):
        copyfile(files[i], folder + '/train/{}.png'.format(i - test))


capture_stream_cv('server/data/{}'.format(input('FaceID: ')))
# capture_stream_from_image_folder_cv('server/data/{}'.format(input('FaceID: ')), input('Folder: '))
# split_data(input('Folder for split: '))
