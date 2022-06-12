from server import app
from flask import render_template, request, send_file
from flask_cors import cross_origin
from jinja2 import TemplateNotFound
import os
from shutil import make_archive, unpack_archive, copyfile
from glob import glob
from .config import Config
from .errors import forbidden_error, not_found_error
from recognition import Detector, CVModel, FaceNetModel
from telegram.server import Bot
from .database import FacesTable
from .facefolder import FaceFolder
'''
    /compile_net    compile_net()       Компилирует FaceNet.
    /load_net       load_net()          Загружает FaceNet.
    /               index()             Возвращает стартовую страницу.
    /<path>         static_file(path)   Возвращает статическую страницу, проверяя статус пользователя и доступ к файлу.
    /upload         upload()            Загружает фото, видео напрямую и из архивов.
    /upload_web     upload_web()        Загружает видео, записанное web-камерой.
    /upload_zip     upload_zip()        Загружает архив с лицами и обучает модель.
    /face/<id>      download_face()     Выгружает параметры лица.
    /data/<id>      download_data()     Выгружает лица, найденные на фото.
    /msg            msg()               Отправляет сообщения от клиентов в бот.
    /add_face       add_face()          Добавляет в БД модели, обученные не через сайт.
'''


@app.route('/compile_net')
@cross_origin()
def compile_net():
    FaceNetModel.compile_net()
    return "OK"


@app.route('/load_net')
@cross_origin()
def load_net():
    FaceNetModel.load_net()
    return "OK"


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


@app.route("/upload", methods=['GET', 'POST'])
@cross_origin()
def upload():
    if request.method == 'GET':
        try:
            face = request.args.get('face')
            return render_template('result.html', url=face)
        except Exception:
            return forbidden_error()

    try:
        files = request.files.getlist("file")
    except Exception:
        return forbidden_error()

    folder = FaceFolder()
    folder.create()
    i = 1
    for file in files:
        extension = file.filename.rsplit('.')[-1]
        if extension in Config.VIDEO_EXTENSIONS:
            name = os.path.join(folder.video(), str(i) + '.' + extension)
        elif extension in Config.IMAGE_EXTENSIONS:
            name = os.path.join(folder.image(), str(i) + '.' + extension)
        elif extension in Config.ARCHIVE_EXTENSIONS:
            name = os.path.join(folder.temp(), str(i) + '.' + extension)
            file.save(name)
            unpack_archive(name, folder.temp(), "zip")
            os.remove(name)
            continue
        else:
            continue
        i += 1
        file.save(name)
    for file in glob(folder.temp() + '/*.*'):
        extension = file.rsplit('.')[-1]
        if extension in Config.VIDEO_EXTENSIONS:
            name = os.path.join(folder.video(), str(i) + '.' + extension)
        elif extension in Config.IMAGE_EXTENSIONS:
            name = os.path.join(folder.image(), str(i) + '.' + extension)
        else:
            continue
        i += 1
        copyfile(file, name)
    folder.clear()
    i = Detector().parse_images(folder.image(), folder.temp())
    Detector().parse_videos(folder.video(), folder.temp(), i, 90)
    make_archive(folder.images_archive(), 'zip', folder.temp())
    folder.clear()
    return render_template('result.html', url=folder.face())


@app.route("/upload_web", methods=['POST'])
@cross_origin()
def upload_web():
    try:
        file = request.files['voice']
        folder = FaceFolder()
        folder.create()
        file.save(folder.video() + '/0.mp4')
        Detector().parse_videos(folder.video(), folder.temp())
        make_archive(folder.images_archive(), 'zip', folder.temp())
        folder.clear()
        return folder.face()
    except Exception:
        return '-'


@app.route("/upload_zip", methods=['POST'])
@cross_origin()
def upload_zip():
    try:
        files = request.files.getlist("file")
        url = request.form['id']
        name = request.form['name']
    except Exception:
        return forbidden_error()

    FacesTable.insert(int(url))
    folder = FaceFolder(url)
    model = FaceNetModel()
    model.name = name

    if len(files) == 0 or len(files) == 1 and files[0].filename == '':
        unpack_archive(folder.images_archive() + '.zip', folder.temp(), "zip")
        model.train(*Detector().get_data(folder.dir(), folder.temp(), False))
        model.write(folder.dir())
        folder.clear()
        return render_template('end.html', url=url)

    i, data = 0, []
    for file in files:
        extension = file.filename.rsplit('.')[-1]
        if extension not in Config.ARCHIVE_EXTENSIONS:
            continue
        name = os.path.join(folder.temp2(), str(i) + '.' + extension)
        i += 1
        file.save(name)
        unpack_archive(name, folder.temp2(), "zip")
        os.remove(name)
    for file in glob(folder.temp2() + '/*.*'):
        extension = file.rsplit('.')[-1]
        if extension not in Config.IMAGE_EXTENSIONS:
            os.remove(file)
    model.train(*Detector().get_data(folder.temp2(), folder.temp(), False))
    model.write(folder.dir())
    folder.clear()
    return render_template('end.html', url=url)


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


@app.route("/msg", methods=['POST'])
@cross_origin()
def msg():
    try:
        text = request.form['text']
        face = int(request.form['face'])
    except Exception:
        return forbidden_error()

    Bot.send_message_server(text, face)
    return render_template('index.html')


@app.route("/add_face", methods=['POST'])
@cross_origin()
def add_face():
    try:
        face = int(request.form['face'])
    except Exception:
        return forbidden_error()

    FacesTable.insert(face)
    return render_template('index.html')
