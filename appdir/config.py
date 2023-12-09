import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))


# current file path (omit the detail .py info), used to find path to put files of courses

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'data.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    BABEL_DEFAULT_LOCALE = 'zh'
    BABEL_DEFAULT_TIMEZONE = 'UTC'
    RESOURCE_UPLOAD_DIR = os.path.join(basedir, "static", "file_sources", "courses")
    PRODUCT_PIC_IMG = os.path.join(basedir, 'static', 'images', 'products')
    PRODUCT_BLOG_IMG = os.path.join(basedir, 'static', 'images', 'blog_img')
    PRODUCT_VIDEO = os.path.join(basedir, 'static', 'images', 'video')

    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_SAMESITE = 'NONE'
    # JWT setting
    # 设置普通JWT过期时间
    # JWT_TOKEN_LOCATION = ["headers", "cookies", "json", "query_string"]
    # JWT_CSRF_IN_COOKIES = False
    # JWT_ACCESS_COOKIE_NAME = "jwt"
    # JWT_SECRET_KEY = "jose"
    # JWT_BLACKLIST_ENABLED = True
    # JWT_COOKIE_CSRF_PROTECT = False
    # JWT_BLACKLIST_TOKEN_CHECKS = ['access']
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=12)
    # 设置刷新JWT过期时间
    # JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)


# Mail Stepup
MAIL_SERVER = 'smtp.qq.com'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USERNAME = '2569787435@qq.com'
MAIL_PASSWORD = 'tdqmqcuxkvendhjg'
MAIL_DEFAULT_SENDER = '2569787435@qq.com'
UPLOADED_PATH = os.path.join(basedir, 'uploads'),
# Flask-Dropzone config:
DROPZONE_ALLOWED_FILE_TYPE = 'image'
DROPZONE_MAX_FILE_SIZE = 3
DROPZONE_MAX_FILES = 30
