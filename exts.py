from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

# 引入Mail()
mail = Mail()
jwt = JWTManager()