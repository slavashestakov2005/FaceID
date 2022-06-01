from server import app
from flask import render_template, request, send_file
from flask_cors import cross_origin
from jinja2 import TemplateNotFound
import os
from shutil import make_archive, unpack_archive, rmtree
from time import time
from .config import Config
from .errors import forbidden_error, not_found_error
from recognition import Detector, CVModel
'''
    generate_folder_name()              Придумывает уникаольное имя для лица.
    /               index()             Возвращает стартовую страницу.
    /<path>         static_file(path)   Возвращает статическую страницу, проверяя статус пользователя и доступ к файлу.
    /upload_image   upload_image()      Загружает фото.
    /upload_video   upload_video()      Загружает видео.
    /upload_zip     upload_zip()        Загружает архив с лицами для обучения модели.
    /face/<id>      download_face()     Выгружает параметры лица.
    /data/<id>      download_data()     Выгружает лица, найденные на фото.
'''


def generate_folder_name():
    s = str(int(time() * 1000))
    return s, os.path.join(Config.DATA_FOLDER, s)


def image_folder(folder):
    return os.path.join(folder, 'image')


def video_folder(folder):
    return os.path.join(folder, 'video')


def temp_folder(folder):
    return os.path.join(folder, 'temp')


def images_archive(folder):
    return os.path.join(folder, 'images')


def cv_model(folder):
    return os.path.join(folder, 'cv.face')


def create_dir(directory, remove_old=True):
    if os.path.exists(directory) and remove_old:
        rmtree(directory)
    video_directory = video_folder(directory)
    image_directory = image_folder(directory)
    temp_directory = temp_folder(directory)
    if not os.path.exists(directory):
        os.makedirs(directory)
    if not os.path.exists(video_directory):
        os.makedirs(video_directory)
    if not os.path.exists(image_directory):
        os.makedirs(image_directory)
    if not os.path.exists(temp_directory):
        os.makedirs(temp_directory)


def clear_dir(directory):
    if os.path.exists(directory):
        rmtree(directory)
    os.makedirs(directory)


@app.route('/')
@cross_origin()
def index():
    return render_template('index.html')


@app.route('/<path:path>')
@cross_origin()
def static_file(path):
    parts = [x.lower() for x in path.rsplit('.', 1)]
    try:
        if len(parts) >= 2 and parts[1] == 'html':
            return render_template(path)
        return app.send_static_file(path)
    except TemplateNotFound:
        return not_found_error()


@app.route("/upload_image", methods=['POST'])
@cross_origin()
def upload_image():
    try:
        files = request.files.getlist("file")
    except Exception:
        return forbidden_error()

    url, directory = generate_folder_name()
    image_directory = image_folder(directory)
    temp_directory = temp_folder(directory)
    create_dir(directory)
    i = 1
    for file in files:
        name = os.path.join(temp_directory, str(i) + '.' + file.filename.rsplit('.')[-1])
        i += 1
        file.save(name)
    Detector().parse_images(temp_directory, image_directory)
    make_archive(images_archive(directory), 'zip', image_directory)
    clear_dir(temp_directory)
    return render_template('index.html', dataurl=url)


@app.route("/upload_video", methods=['POST'])
@cross_origin()
def upload_video():
    try:
        files = request.files.getlist("file")
    except Exception:
        return forbidden_error()

    url, directory = generate_folder_name()
    video_directory = video_folder(directory)
    image_directory = image_folder(directory)
    create_dir(directory)
    i = 1
    for file in files:
        name = os.path.join(video_directory, str(i) + '.' + file.filename.rsplit('.')[-1])
        i += 1
        file.save(name)
    Detector().parse_videos(video_directory, image_directory, 90)
    make_archive(images_archive(directory), 'zip', image_directory)
    return render_template('index.html', dataurl=url)


@app.route("/upload_zip", methods=['POST'])
@cross_origin()
def upload_zip():
    try:
        files = request.files.getlist("file")
    except Exception:
        return forbidden_error()

    url, directory = generate_folder_name()
    temp_directory = temp_folder(directory)
    image_directory = image_folder(directory)
    create_dir(directory)
    i, data = 1, []
    for file in files:
        name = os.path.join(temp_directory, str(i) + '.' + file.filename.rsplit('.')[-1])
        i += 1
        file.save(name)
        unpack_archive(name, temp_directory, "zip")
        os.remove(name)
    model = CVModel()
    model.train(*Detector().get_data(directory, image_directory))
    model.write(directory)
    make_archive(images_archive(directory), 'zip', image_directory)
    return render_template('index.html', url=url)


@app.route("/face/<int:face>")
@cross_origin()
def download_face(face):
    file = './data/{}/cv.face'.format(face)
    return send_file(file, as_attachment=True, attachment_filename='{}.face'.format(face))


@app.route("/data/<int:face>")
@cross_origin()
def download_data(face):
    file = './data/{}/images.zip'.format(face)
    return send_file(file, as_attachment=True, attachment_filename='{}.zip'.format(face))
