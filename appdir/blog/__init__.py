from flask import Blueprint

blog = Blueprint('blog', __name__, )

from appdir.blog import views
