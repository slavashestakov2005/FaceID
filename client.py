from recognition.videostream import capture_stream
# from recognition.tester import test


# test()
capture_stream('server/data/{}'.format(input('FaceID: ')))
# capture_stream_from_image_folder('server/data/{}'.format(input('FaceID: ')), input('Folder: '))
# folder = input('Folder for split: ')
# while True:
#     split_data(folder,  chose_count=int(input('Count of images: ')))
