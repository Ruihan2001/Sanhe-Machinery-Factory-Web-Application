from flask import Blueprint

staff = Blueprint('staff', __name__, )

from appdir.staff import views
