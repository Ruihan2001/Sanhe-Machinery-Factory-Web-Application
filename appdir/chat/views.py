import datetime
import json
import os
import re
import sys
import requests
from appdir.chat import chat

from flask import render_template, redirect, request, url_for, session

from appdir.sanhe.models import User


@chat.route('/index')
def index():
    return render_template('layout/chat_ai.html')


@chat.route('/index2')
def index2():
    return render_template('chat/chat_ai.html')


@chat.route('/index/<userid>')
def index_with_jwt(userid):
    user = User.query.filter_by(unionid=userid).first()
    if user:
        return render_template('chat/chat_ai.html', user=user)
    else:
        return render_template('chat/chat_ai.html')
