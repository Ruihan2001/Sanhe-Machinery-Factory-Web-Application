import os
# if you want to execute the program by python interpreter
# please run this file
from flask_dropzone import Dropzone
from appdir import app

dropzone = Dropzone(app)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)


    # app.run(host='0.0.0.0', port=10000, debug=True)
    # app.run(host='0.0.0.0', port=443, debug=True, ssl_context=('nginx.pem', 'nginx.key'))
    # app.run(host='0.0.0.0')

# pip install Flask==2.0.2
# pip install Flask_SQLAlchemy==2.5.1
# pip install Flask_WTF==0.15.1
# pip install Werkzeug==2.0.2
# pip install WTForms==2.3.3
# pip install flask_babel
# pip install email_validator
# pip install flask_dropzone
# pip install flask_dropzone
# pip install opencv-python
# pip install flask-mail==0.9.1
