import json
import sys
import string, random

from flask_babel import gettext as _

import requests
from prometheus_flask_exporter import PrometheusMetrics
from sqlalchemy import func

from appdir.sanhe import sanhe
from werkzeug.security import generate_password_hash, check_password_hash
from flask import render_template, redirect, request, url_for, session, g, views, jsonify, make_response, flash

from appdir.sanhe.forms import LoginForm, RegisterForm, LoginFormForAdminister, ResetEmailForm
from appdir.sanhe.models import User, Products, Pro_Image, Wishlist, Pro_Video

from utils import restful
from bs4 import BeautifulSoup
from flask_mail import Message
from exts import mail
from appdir import db, metrics
from appdir.sanhe.forms import ValidationError, RegisterForm

from flask_jwt_extended import create_access_token, set_access_cookies, unset_jwt_cookies
from flask_jwt_extended import create_refresh_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required

by_path_counter = metrics.counter(
    'by_path_counter', 'Request count by request paths',
    labels={'path': lambda: request.path}
)


def xml_parse(text):
    result = {}
    soup = BeautifulSoup(text, 'html.parser')
    tag_list = soup.find(name='error').find_all()
    for tag in tag_list:
        result[tag.name] = tag.text
    return result


@sanhe.route('/')
def sanhe_none():
    if request.method == 'GET':
        redirect_to_home = url_for(('sanhe.homepage'))
        return redirect(redirect_to_home)


@sanhe.route('/factory')
def sanhe_model():
    return render_template('model/走动模式.html')


@sanhe.route('/factory2')
def sanhe_model2():
    return render_template('model/飞翔模式.html')


@sanhe.route('/vr')
def sanhe_vr():
    # response = jsonify({"msg": "login successful not none"})
    # access_token = create_access_token(identity="user.id")
    # set_access_cookies(response, access_token)
    # return response
    return render_template('vr.html')


@sanhe.route('/auth/weixin_signin', methods=['GET', 'POST'])
def login_by_wechat():
    print(request.args, file=sys.stderr)
    print(request.args.get("code"), file=sys.stderr)
    code = request.args.get("code")
    redirect_url = ""
    ru = requests.get(url=redirect_url)
    if "errcode" in ru.text:
        # TODO Error Info
        return "error todo" + str(ru.text)

    print(ru, file=sys.stderr)
    print(ru.text, file=sys.stderr)
    access_dict = json.loads(ru.text)
    access_token = access_dict["access_token"]
    openid = access_dict["openid"]
    user_info_url = "https://api.weixin.qq.com/sns/userinfo?access_token=" + access_token + "&openid=" + openid
    ru = requests.get(url=user_info_url)
    result_dict = json.loads(ru.text)

    sex = result_dict["sex"]
    nickname = result_dict["nickname"].encode("ISO-8859-1").decode("utf-8")
    headimgurl = result_dict["headimgurl"]
    unionid = result_dict["unionid"]

    user = User.query.filter_by(unionid=unionid).first()
    if user is None:
        user = User(nickname=nickname, sex=sex, headimgurl=headimgurl, unionid=unionid)
        db.session.add(user)
        db.session.commit()
        # fetch again
        user = User.query.filter_by(unionid=unionid).first()
        session['id'] = user.unionid
        return redirect(url_for("sanhe.login_set_cookie", user_id=user.unionid))
    else:
        return redirect(url_for("sanhe.login_set_cookie", user_id=user.unionid))
    # response = Response('Not Found', status=404)
    # return redirect(url_for("sanhe.homepage"))


@sanhe.route('/auth/log_result/<user_id>', methods=['GET', 'POST'])
def login_result(user_id):
    return render_template('login_result.html', user_id=user_id)


@sanhe.route('/set_jwt_cookie/<user_id>', methods=['GET', 'POST'])
def login_set_cookie(user_id):
    # user = User.query.filter_by(unionid=user_id).first()
    path = '/sanhe/auth/log_result/' + str(user_id)
    response = make_response(redirect(path))
    # access_token = create_access_token(identity=user_id)
    # set_access_cookies(response, access_token)
    return response


@sanhe.route('/auth/<operation_type>', methods=['GET', 'POST'])
def login(operation_type):
    form_login = LoginForm()
    form_signup = RegisterForm()
    form_login_ad = LoginFormForAdminister()
    move_to_login = render_template('login_signup.html', form_login=form_login, form_login2=form_login_ad,
                                    form_signup=form_signup)
    redirect_to_login = url_for('sanhe.login', operation_type="login")
    if request.method == 'GET':
        username = session.get("111")
        if username is None:
            return move_to_login
        else:
            # if the user has login in, there is item saved in session, we bring him to main course page directly
            next_main = url_for('sanhe.homepage')
            return redirect(next_main)
    if request.method == 'POST':
        if operation_type == "login":
            name = request.form.get("name")
            password = request.form.get("password")
            if name is not None:
                user_in_db = User.query.filter_by(email=name).first()
                if not user_in_db:
                    # no such user return 1
                    return jsonify({'returnValue': 1})
                print(user_in_db.email)

                if check_password_hash(user_in_db.password_hash, password):
                    print("password pass")
                    session["user_id"] = user_in_db.id
                    session["USERNAME"] = user_in_db.email
                    unicode = user_in_db.unionid
                    # if user_in_db.authority == 0:
                    session["TYPE"] = "user"
                    # else:
                    #     session["TYPE"] = "manager"
                    # session.permanent = True
                    flash(_("login successfully"))
                    return jsonify({'user_unicode': unicode, "result": "success"})
                    return redirect(url_for("sanhe.login_set_cookie", user_id=unicode))
                else:
                    return jsonify({'returnValue': 2})
            # print(1)
            return redirect(redirect_to_login)

        # when the post request is sent from user finish form for login
        # if operation_type == "login":
        #     form_username = form_login.username.data
        #     form_password = form_login.password.data
        #
        #     return redirect(url_for("sanhe.user_profile"))
        #     if form_login.validate_on_submit() and form_login.validate_username_not_exist(form_login.username):
        #         user = User.query.filter_by(username=form_username).first()
        #         if check_password_hash(user.password_hash, form_password) is False:
        #             # app.logger.error("user login failed for entering wrong password")
        #             # flash("wrong username or password")
        #             return redirect(redirect_to_login)
        #         # user is not None and correct password, move to main course page
        #         else:
        #             session["USERNAME"] = user.username
        #             # set the time for the session length (default one month)
        #             if form_login.remember_me.data:
        #                 session.permanent = True
        #             else:
        #                 session["USERNAME"] = user.username
        #             # access_token = create_access_token(identity="example_user")
        #             # next_main = url_for('sanhe.user_profile', access_token)
        #             # return redirect(next_main)
        #     return redirect(redirect_to_login)
        # # when the post request is sent from user finish form for register
        # elif operation_type == "signup":
        #     form_username = form_signup.username.data
        #     form_password = form_signup.password.data
        #     if form_signup.validate_on_submit() and form_signup.validate_username_exist(form_signup.username):
        #         # flash("Register successfully: Your username: {}".format(form_signup.username.data))
        #         # we have use form_signup.validate_username_exist(form_signup.username) to detect the user is not exist
        #         # put user into database
        #         user = User(username=form_username, nickname=form_username,
        #                     password_hash=generate_password_hash(form_password))
        #         db.session.add(user)
        #         db.session.commit()
        #         return redirect(redirect_to_login)
        # elif operation_type == "login2":
        #     if form_login_ad.validate_on_submit():
        #         # when the post request is sent from administrator finish form for login
        #         form_username = form_login_ad.username.data
        #         form_password = form_login_ad.password.data
        #         user = User.query.filter_by(username=form_username, role=1).first()
        #         if user is None:
        #             return move_to_login
        #         elif check_password_hash(user.password_hash, form_password) is False:
        #             # app.logger.error('Warning Administrator password')
        #             return move_to_login
        #         # user is not None and correct password, move to main course page
        #         else:
        #             # app.logger.info('Administrator has login')
        #             session["ROLE"] = "Administrator"
        #             # next_main = url_for('manage_database', mode_type="user", page=1)
        #             # return redirect(next_main)
        return redirect(redirect_to_login)


@sanhe.route('/auth/reset')
def resetpassword():
    return render_template('resetpassword.html', language="en")


# bring user to login, if he directly visit the root directory)
@sanhe.route('/index')
@jwt_required(optional=True)
def homepage():
    current_user = get_jwt_identity()
    print(current_user, file=sys.stderr)
    # user = User.query.filter_by(unionid=current_user).first()
    if current_user:
        return render_template('homepage.html', userid=current_user, language="en")
    else:
        return render_template('homepage.html', language="en")


@sanhe.route('/index_zh-cn')
def homepage_zh():
    return render_template('homepage_zh.html', language="zh-cn")


@sanhe.route('/products')
def products():
    product = Products.query.all()
    return render_template('products.html', product=product, language="en")


@sanhe.route('/products_zh-cn')
def products_zh():
    return render_template('products_zh.html', language="zh-cn")


@sanhe.route('/products/automatic_production_line')
def product1():
    return render_template('product_1.html', language="en")


@sanhe.route('/products/automatic_production_line_zh-cn')
def product1_zh():
    return render_template('product_1_zh.html', language="zh-cn")


@sanhe.route('/products/log_frame_saw_machine')
def product2():
    return render_template('product_2.html', language="en")


@sanhe.route('/products/log_frame_saw_machine_zh-cn')
def product2_zh():
    return render_template('product_2_zh.html', language="zh-cn")


@sanhe.route('/products/square_frame_saw_machine')
def product3():
    return render_template('product_3.html', language="en")


@sanhe.route('/product_detail/<product_name>')
@jwt_required(optional=True)
def product_detail(product_name):
    current_user = get_jwt_identity()
    product = Products.query.filter_by(product_route=product_name).first()
    # print(product.product_id)
    imgs = Pro_Image.query.filter_by(imgProduct_id=product.product_id)
    videos = Pro_Video.query.filter_by(videoProduct_id=product.product_id).all()
    recommends = Products.query.filter(Products.product_name != product.product_name,
                                       Products.product_category == product.product_category).all()

    recommends2 = []

    status = Wishlist.query.filter_by(user_id=current_user, product_id=product.product_id).first()
    if status:
        collection = "collected"
        # print("collected")
    else:
        collection = "uncollected"
        # print("uncollected")

    return render_template('product_detail.html', product=product,
                           recommends=recommends,
                           imgs=imgs,
                           videos=videos,
                           collection=collection,
                           user=current_user)


# @sanhe.route('/product_detail/square_frame_saw_machine_zh-cn')
# def product3_zh():
#     return render_template('product_3_zh.html', language="zh-cn")
#
#
# @sanhe.route('/product_detail/tea_twisting_machine')
# def product4():
#     return render_template('product_rounian.html', language="en")
#
#
# @sanhe.route('/product_detail/tea_twisting_machine_zh-cn')
# def product4_zh():
#     return render_template('product_rounian_zh.html', language="zh-cn")


@sanhe.route('/news')
def news():
    return render_template('index_fullscreen.html', language="en")


@sanhe.route('/news_zh-cn')
def news_zh():
    return render_template('index_fullscreen_zh.html', language="zh-cn")


@sanhe.route('/contact')
def contact():
    return render_template('contact.html', language="en")


@sanhe.route('/contact_zh-cn')
def contact_zh():
    return render_template('contact_zh.html', language="zh-cn")


@sanhe.route('/faqs')
def faqs():
    return render_template('faqs.html', language="en")


@sanhe.route('/faqs_zh-cn')
def faqs_zh():
    return render_template('faqs_zh.html', language="zh-cn")


# # random
# source = list(string.ascii_letters)
# source.extend(map(lambda x: str(x), range(0, 10)))
# random.sample(source, 6)
# captcha = "".join(random.sample(source, 6))


@sanhe.route('/auth/email_captcha/')
def email_captcha():
    # 获取要修改的邮箱
    email = request.args.get('email')
    if not email:
        return restful.params_error('Please enter your email address')
    source = list(string.ascii_letters)
    source.extend(map(lambda x: str(x), range(0, 10)))
    captcha = "".join(random.sample(source, 6))
    message = Message(subject='SANHE-Verification Code', sender='2569787435@qq.com', recipients=[email],
                      body='Your verification code is %s' % captcha)
    # message.html = render_template('email_template.html')
    try:
        mail.send(message)
    except:
        return restful.server_error(message)
    # zlcache.set(email,captcha)
    session["code"] = captcha
    return restful.success()


@sanhe.route('/auth/verification/')
def verification():
    # def get(self):
    #     return render_template(url_for("appdir/templates/login_signup.html"))
    #
    # def post(self):
    input_code = request.args.get("captcha")
    username = request.args.get("email")
    userpw = request.args.get("userpw")
    code = session.get("code")
    # print(userpw)
    # print(input_code, code)
    if input_code != code:
        return restful.params_error("Wrong Code")
    else:
        unionid = ''.join(random.choices(string.ascii_letters + string.digits + '_', k=30))
        # print(unionid)
        user = User(nickname="Anonymous User", unionid=unionid,
                    headimgurl='/static/images/avatar/300-' + str(random.randint(1, 11)) + '.jpg',
                    email=username, password_hash=generate_password_hash(userpw))
        db.session.add(user)
        db.session.commit()
        return restful.success(message=unionid)

    # if form.validate():
    #     email = form.email.data
    #     g.cms_user.email = email
    #     return restful.success()
    # else:
    #     return restful.params_error(form.get_error())


# @sanhe.route('/user-profile')
# def user_profile():
#     return render_template('user.html', language="en")
#
# @sanhe.route('/user-profile_zh-cn')
# def user_profile():
#     return render_template('user_zh.html', language="zh-cn")

@sanhe.route('/user/set_jwt', methods=["POST", "GET"])
def user_jwt():
    user_id = request.args.get("user_id")
    access_token = create_access_token(identity=user_id)
    output = jsonify({'refresh': True})
    resp = make_response(output)
    resp.set_cookie('jwt', access_token)
    return resp


@sanhe.route('/user/get_jwt', methods=["POST", "GET"])
@jwt_required(optional=True)
def user_get_jwt():
    current_user = get_jwt_identity()
    output = jsonify({'refresh': True, "current_user": current_user})
    resp = make_response(output)
    return resp


# userid = None

@sanhe.route('/user/change/name', methods=["POST"])
@jwt_required()
def user_change_nickname():
    current_user_id = get_jwt_identity()
    current_user = User.query.filter_by(unionid=current_user_id).first()
    print(request.args.get("changed_name"))
    if current_user:
        changed_name = request.args.get("changed_name")
        if changed_name:
            current_user.nickname = changed_name
            db.session.commit()
            return restful.success()
        return restful.params_error(message="no changed name")
    return restful.params_error(message="no login")


@sanhe.route('/user/profile/<user_id>', methods=["GET"])
@jwt_required()
def user_profile(user_id):
    if request.method == 'GET':
        # global userid
        user = User.query.filter_by(unionid=user_id).first()
        userid = user.unionid
        # return jsonify(logged_in_as=access_token)
        if user:
            wishlist = Wishlist.query.filter_by(user_id=user_id).all()
            products = []

            for wish in wishlist:
                product = Products.query.filter_by(product_id=wish.product_id).first()
                products.append(product)

            return render_template("user/user_profile.html", products=products, user=user)
            # return jsonify(logged_in_as=current_identity)
        else:
            return jsonify(logged_in_as="anonymous user")


@sanhe.route('/user/profile/set_jwt/<userid>', methods=["GET"])
def user_profile_set_jwt(userid):
    if request.method == 'GET':
        path = '/sanhe/user/profile/' + str(userid)
        response = make_response(redirect(path))
        access_token = create_access_token(identity=userid)
        set_access_cookies(response, access_token)
        return response


@sanhe.route('/user/forget_pw')
def user_forget_pw():
    if request.method == 'GET':
        return render_template("user/user_profile.html")


@sanhe.route("/logout_with_cookies", methods=["GET", "POST"])
def logout_with_cookies():
    path = '/sanhe/auth/login'
    response = make_response(redirect(path))
    unset_jwt_cookies(response)
    return response


@sanhe.route("/logout_with_cookies/homepage", methods=["GET", "POST"])
def logout_with_cookies_homepage():
    path = '/sanhe/index'
    response = make_response(redirect(path))
    unset_jwt_cookies(response)
    return response


@sanhe.route('/user/close_news/', methods=["POST"])
@jwt_required(optional=True)
def close_news():
    current_user_id = get_jwt_identity()
    print("current_user_id", current_user_id, file=sys.stderr)

    if current_user_id:
        # csrf_token = get_jwt()["csrf"]
        current_user = User.query.filter_by(unionid=current_user_id).first()
        if current_user.adv_accept:
            current_user.adv_accept = False
            db.session.commit()
    return restful.success()


@sanhe.route('/user/open_news/', methods=["POST"])
@jwt_required(optional=True)
def open_news():
    current_user_id = get_jwt_identity()
    print("current_user_id", current_user_id, file=sys.stderr)

    if current_user_id:
        # csrf_token = get_jwt()["csrf"]
        current_user = User.query.filter_by(unionid=current_user_id).first()
        if not current_user.adv_accept:
            current_user.adv_accept = True
            db.session.commit()
    return restful.success()


@sanhe.route("/user/bind_email", methods=["GET", "POST"])
@jwt_required()
def user_bind_email():
    return render_template('user/email_bind.html')


@sanhe.route('/user/bind_email/email/')
def bind_email_captcha():
    # 获取要修改的邮箱
    email = request.args.get('email')
    if not email:
        return restful.params_error('Please enter your email address')
    source = list(string.ascii_letters)
    source.extend(map(lambda x: str(x), range(0, 10)))
    captcha = "".join(random.sample(source, 6))
    message = Message(subject='SANHE-Verification Code-Binding Email', sender='2569787435@qq.com', recipients=[email],
                      body='Your verification code is %s' % captcha)
    # message.html = render_template('email_template.html')
    try:
        mail.send(message)
    except:
        return restful.server_error(message)
    # zlcache.set(email,captcha)
    session["code"] = captcha
    return restful.success()


@sanhe.route('/user/bind_email/verification/')
def bind_verification():
    # def get(self):
    #     return render_template(url_for("appdir/templates/login_signup.html"))
    #
    # def post(self):
    email = request.args.get('email')
    input_code = request.args.get("captcha")
    userpw = request.args.get("userpw")
    code = session.get("code")
    print(userpw)
    print(input_code, code)
    if input_code != code:
        return restful.params_error("Wrong Code")
    else:
        user = User.query.filter_by(unionid=userid).first()
        user.email = email
        user.password_hash = generate_password_hash(userpw)
        # user = User(email=username, password_hash=generate_password_hash(userpw))
        # db.session.add(user)
        db.session.commit()
        return restful.success()


@sanhe.route('/product_detail/collection/', methods=['POST'])
@jwt_required()
def collection():
    # user0 = User.query.filter_by(unionid=userid).first()
    userid = get_jwt_identity()
    print(userid)
    product_id = request.json.get('product_id')
    action = request.json.get('action')
    product = Wishlist.query.filter_by(user_id=userid, product_id=product_id).first()
    # if not user0:
    #     return restful.params_error("No such user!")
    if action == 'collect':
        if not product:
            Collection = Wishlist(user_id=userid, product_id=product_id)
            db.session.add(Collection)
            db.session.commit()
            restful.success()
        else:
            restful.params_error("Unsuccessfully!")
    if action == 'uncollect':
        if product:
            print("ok")
            db.session.delete(product)
            db.session.commit()

    return restful.success()
