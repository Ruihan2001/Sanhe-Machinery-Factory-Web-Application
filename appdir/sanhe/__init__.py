from flask import Blueprint

sanhe = Blueprint('sanhe', __name__, )

from appdir.sanhe import views

