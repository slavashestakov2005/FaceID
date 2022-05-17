from server import app
from flask import render_template, request, send_file
from flask_cors import cross_origin
from jinja2 import TemplateNotFound
import os
from time import time
from .config import Config
from .errors import forbidden_error, not_found_error
from recognition import train_cv, capture_stream_cv
'''
    generate_folder_name()              Придумывает уникаольное имя для лица.
    /               index()             Возвращает стартовую страницу.
    /<path>         static_file(path)   Возвращает статическую страницу, проверяя статус пользователя и доступ к файлу.
    /upload         upload()            Загружает фото.
    /face/<id>      download_face()     Выгружает параметры лица.
'''


def generate_folder_name():
    s = str(int(time() * 1000))
    return s, os.path.join(Config.DATA_FOLDER, s)


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


@app.route("/upload", methods=['POST'])
@cross_origin()
def upload():
    try:
        files = request.files.getlist("file")
    except Exception:
        return forbidden_error()

    url, directory = generate_folder_name()
    if not os.path.exists(directory):
        os.makedirs(directory)
    i = 1
    for file in files:
        name = os.path.join(directory, str(i) + '.' + file.filename.rsplit('.')[-1])
        i += 1
        file.save(name)
    face = train_cv(directory)
    capture_stream_cv(face)
    return render_template('index.html', url=url)


@app.route("/face/<int:face>")
@cross_origin()
def download_face(face):
    file = './data/{}.face'.format(face)
    return send_file(file, as_attachment=True, attachment_filename='{}.face'.format(face))
