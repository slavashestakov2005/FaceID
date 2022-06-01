from recognition.videostream import capture_stream_cv


capture_stream_cv('server/data/{}'.format(input('FaceID: ')))
# capture_stream_from_image_folder_cv('server/data/{}'.format(input('FaceID: ')), input('Folder: '))
# folder = input('Folder for split: ')
# while True:
#     split_data(folder,  chose_count=int(input('Count of images: ')))
