from flask import Blueprint

chat = Blueprint('chat', __name__, )

from appdir.chat import views
