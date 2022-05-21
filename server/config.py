class Config:
    UPLOAD_FOLDER = 'server/static'
    TEMPLATES_FOLDER = 'server/templates'
    EXAMPLES_FOLDER = 'server/examples'
    DATA_FOLDER = 'server/data'
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'mp4'])
    SECRET_KEY = 'you-will-never-guess'
    TEMPLATES_AUTO_RELOAD = True
