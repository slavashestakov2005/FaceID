class Config:
    UPLOAD_FOLDER = 'server/static'
    TEMPLATES_FOLDER = 'server/templates'
    EXAMPLES_FOLDER = 'server/examples'
    DATA_FOLDER = 'server/data'
    ARCHIVE_EXTENSIONS = {'zip'}
    VIDEO_EXTENSIONS = {'mp4'}
    IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4'}
    SECRET_KEY = 'you-will-never-guess'
    TEMPLATES_AUTO_RELOAD = True
    DB = 'server/database.db'
    DB_COLS_PREFIX = ''
    DB_TABLE_PREFIX = ''
    DROP_DB = False
