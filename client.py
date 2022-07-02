from recognition.videostream import capture_stream_from_image_folder
# from recognition.tester import test
from recognition.fn import FaceNetModel


FaceNetModel.load_net()
# test()
# capture_stream('server/data/{}'.format(input('FaceID: ')))
capture_stream_from_image_folder('server/data/{}'.format(input('FaceID: ')), input('Folder: '))
# folder = input('Folder for split: ')
# while True:
#     split_data(folder,  chose_count=int(input('Count of images: ')))
