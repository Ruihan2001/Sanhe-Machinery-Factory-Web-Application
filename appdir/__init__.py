# The purpose of this file is to construct an application package to call factory functions
import logging
from flask import Flask, jsonify, request, Blueprint, redirect, url_for, render_template
from flask_migrate import Migrate

from appdir.config import Config
from flask_babel import Babel
from exts import mail, jwt

from sqlalchemy import MetaData
from flask_sqlalchemy import SQLAlchemy

from flask_jwt_extended import JWTManager
from prometheus_flask_exporter import PrometheusMetrics
from prometheus_client import CollectorRegistry, make_wsgi_app

from flask_jwt_extended import JWTManager

# log setting
# handler = logging.FileHandler('log-file.log', encoding='UTF-8')
# logging_format = logging.Formatter(
#     '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
# handler.setFormatter(logging_format)
# app.logger.addHandler(handler)

# try:
#     code may appear error
# except Exception as e:
#     app.logger.error('%s', e)

app = Flask(__name__)
babel = Babel(app)
app.config.from_object(Config)
app.config['MAIL_SERVER'] = 'smtp.qq.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = '2569787435@qq.com'
app.config['MAIL_PASSWORD'] = 'tdqmqcuxkvendhjg'
app.config['MAIL_DEFAULT_SENDER'] = '2569787435@qq.com'

app.config["JWT_TOKEN_LOCATION"] = ["headers", "cookies", "json", "query_string"]
app.config["JWT_COOKIE_SECURE"] = False
app.config["JWT_COOKIE_CSRF_PROTECT"] = False
app.config['JWT_CSRF_CHECK_FORM'] = False
app.config["JWT_CSRF_IN_COOKIES"] = False
app.config["JWT_SECRET_KEY"] = "super-secret"
app.config["JWT_ACCESS_COOKIE_NAME"] = "jwt"

# jwt = JWTManager(app)

convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(app, metadata=metadata)

# metrics = PrometheusMetrics(app, path="/metric")
# registry = CollectorRegistry(auto_describe=True)
# metrics = PrometheusMetrics.for_app_factory(registry=registry)
metrics = PrometheusMetrics(app,
                            excluded_paths=".*.js|.*.gif|.*.css|.*.mp4|.*.jpg|.*.png|.*.svg|.*.ico|.*.woff|.*.ttf",
                            # exclude_user_defaults=False,
                            # export_defaults=False,
                            )

# metrics.register_default(
#     metrics.histogram('by_path_counter2', 'Request count by request paths',
#                       labels={'path': lambda: request.path})
# )

metrics_wsgi_app = make_wsgi_app()

# with app.app_context():
migrate = Migrate(app, db, render_as_batch=True)
mail.init_app(app)
jwt.init_app(app)


# db.init_app(app)

@jwt.unauthorized_loader
def my_unauthorized_token_callback(jwt_header):
    """未传头部Authorization"""
    return jsonify(err="Missing Authorization Header"), 401


from appdir.base import base
from appdir.sanhe import sanhe
from appdir.blog import blog
from appdir.staff import staff
from appdir.chat import chat

app.register_blueprint(blog, url_prefix='/blog')
app.register_blueprint(chat, url_prefix='/chat')
app.register_blueprint(staff, url_prefix='/staff')
app.register_blueprint(sanhe, url_prefix='/sanhe')
app.register_blueprint(base, url_prefix='/')


def page_not_found(e):
    return render_template('404.html'), 404


app.register_error_handler(404, page_not_found)


@jwt.expired_token_loader
def my_expired_token_callback(jwt_header, jwt_payload):
    redirect_to_login = url_for(('sanhe.login'), operation_type="login",
                                extra_info="Your Login Has Been Expired! Please Login Again")
    return redirect(redirect_to_login)


@jwt.unauthorized_loader
def unauthorized_callback(err_str):
    redirect_to_login = url_for(('sanhe.login'), operation_type="login", extra_info="Please Login Firstly!")
    return redirect(redirect_to_login)


# db.create_all()
# metrics.init_app(app)

@app.get('/metrics')
@metrics.do_not_track()
def metric():
    return metrics_wsgi_app

# metrics.start_http_server(10000, host="127.0.0.1")
