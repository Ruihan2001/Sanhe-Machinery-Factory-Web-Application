import email
import os
import re
from datetime import datetime
# import cv2
from email import encoders
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.utils import parseaddr
from operator import and_
from os.path import join

from bs4 import BeautifulSoup
from flask_mail import Message
from sqlalchemy import func, or_

import appdir
from appdir import Config
from appdir.staff import staff
from exts import mail
from utils import restful
from .models import Advs
from ..sanhe.models import Products, Pro_Image, User, Pro_Video
from ..blog.models import Comment
from flask import jsonify, render_template, request
from email.header import Header
from appdir.utils.sta_tool import *

from ..blog.models import Blog, Image
from appdir import db

import json

from flask_jwt_extended import create_access_token, set_access_cookies
from flask_jwt_extended import create_refresh_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required


@staff.route('/')
@staff.route('/index', methods=['GET', 'POST'])
@jwt_required()
def index():
    # current_identity = get_jwt_identity()
    # if current_identity:
    #     return jsonify(logged_in_as=current_identity)
    # else:
    #     return jsonify(logged_in_as="anonymous user")

    # index of staff
    # staff_name = session.get("USERNAME")
    news_count = Blog.query.all()
    products_count = Products.query.all()
    return render_template('staff/index.html', title="Staff Index", page="dashboard",
                           products_count=len(products_count),
                           news_count=len(news_count))


@staff.route('/add_products', methods=['GET', 'POST'])
@jwt_required()
def add_products():
    # index of staff
    # staff_name = session.get("USERNAME")
    return render_template('staff/add-product.html', title="Add Product", page="add_product")


@staff.route('/products', methods=['GET', 'POST'])
@jwt_required()
def products():
    # index of staff
    # staff_name = session.get("USERNAME")
    return render_template('staff/all-products.html', title="Staff Products", page="grid_product")


@staff.route('/edit_products', methods=['GET', 'POST'])
@jwt_required()
def products_edit():
    # index of staff
    # staff_name = session.get("USERNAME")
    return render_template('staff_products_edit.html', title=f"Staff Edit Products")


@staff.route('/all_news', methods=['GET', 'POST'])
@jwt_required()
def all_blogs():
    # index of staff
    # staff_name = session.get("USERNAME")
    blog_all = Blog.query.all()
    for blog in blog_all:
        blog.blog_content = BeautifulSoup(blog.blog_content).get_text()
    blog_num = len(blog_all)
    # index of staff
    return render_template('staff/all-news.html', title="All News", news=blog_all, page='news')


@staff.route('/post_news', methods=['GET', 'POST'])
@jwt_required()
def add_blog():
    # index of staff
    # staff_name = session.get("USERNAME")
    return render_template('staff/add-post.html', title="Staff Post News", page='post_news', name="111")


@staff.route('/wait_audit', methods=['GET', 'POST'])
@jwt_required()
def audit_comments():
    comments = Comment.query.filter_by(audited=None).all()
    return render_template('staff/comment-management.html', title="Staff Post News", page='wait_audit_comments',
                           comments=comments)


@staff.route('/passed_comments', methods=['GET', 'POST'])
@jwt_required()
def passed_comments():
    comments = Comment.query.filter(and_(Comment.fake_score == 0, Comment.audited == '1')).all()
    return render_template('staff/comment-management.html', title="Staff Post News", page='passed_comments',
                           comments=comments)


@staff.route('/blocked_comments', methods=['GET', 'POST'])
@jwt_required()
def blocked_comments():
    comments = Comment.query.filter(Comment.audited == '0').all()
    return render_template('staff/comment-management.html', title="Staff Post News", page='blocked_comments',
                           comments=comments)


@staff.route('/edit_blog', methods=['GET', 'POST'])
@jwt_required()
def edit_blog():
    return render_template('staff_blog_edit.html', title="Staff Edit Blog")


@staff.route('/manage_blog', methods=['GET', 'POST'])
@jwt_required()
def manage_blog():
    # index of staff
    # staff_name = session.get("USERNAME")
    return render_template('staff_blog_manage.html', title="Staff Manage Blog")


# @staff.route('/test', methods=['GET', 'POST'])
# def test():
#     # index of staff
#     # staff_name = session.get("USERNAME")
#     return render_template('staff/test.html', title="Staff Manage Blog")


@staff.route('/get_id', methods=['POST'])
def get_id():
    pre_id = produce_id()
    final_id_flag = False
    same_num = 0
    while final_id_flag != True:
        final_id = pre_id + str(same_num)
        if Blog.query.filter_by(id=final_id).first() is None:
            final_id_flag = True
            final_id = final_id
        else:
            same_num += 1
    print(final_id)
    return {"id": final_id}


@staff.route('/post_blog', methods=['GET', 'POST'])
@jwt_required()
def postBlog():
    current_user_id = get_jwt_identity()
    current_user = User.query.filter_by(unionid=current_user_id).first()

    if current_user:
        content = request.form.get('content')
        title = request.form.get('title')
        final_id = request.form.get('final_id')
        blog_category = request.form.get('tags')
        date = request.form.get('date')
        imgs = request.form.get('img_list')

        blog = Blog(id=final_id,
                    blog_content=content,
                    blog_title=title,
                    blog_category=blog_category,
                    blog_time=date,
                    author=current_user.nickname,
                    author_avatar=current_user.headimgurl)
        db.session.add(blog)
        db.session.commit()
        img_list = imgs.split(",")
        for i in img_list:
            img = Image(imgBlog_id=final_id,
                        img_path=i)
            db.session.add(img)
            db.session.commit()
        if img_list:
            blog.blog_image_route = '/static/images/blog_img/' + img_list[0]
            db.session.commit()
        return {"id": 'success'}


def formatAddr(s):
    name, addr = parseaddr(s)
    return formatAddr((Header(name, 'utf-8').encode().addr))


@staff.route('/post_adv', methods=['GET', 'POST'])
def postAdv():
    content = request.args.get('content')
    title = request.args.get('title')
    final_id = request.args.get('final_id')
    blog_category = request.args.get('tags')
    date = request.args.get('date')
    image = request.args.get('img_list')
    img_list = []
    for i in image.split(","):
        if i != "":
            img_list.append(i)
    print(img_list)

    # adv = Advs(id=final_id,
    #            adv_content=content,
    #            adv_title=title,
    #            adv_category=blog_category,
    #            adv_time=date,
    #            adv_image_route=image)
    # db.session.add(adv)
    # db.session.commit()
    # email_receive=User.query.get(email)

    adv_users = User.query.filter_by(adv_accept=True).all()
    email_list = []
    for user in adv_users:
        if user.email:
            email_list.append(user.email)

    message = Message(subject='SANHE NEWS', sender='2569787435@qq.com',
                      recipients=['1053924276@qq.com'], bcc=email_list, body="Hello")

    # fp = open("appdir/static/images/logo-white.png")
    # images = MIMEImage(fp.read())
    # fp.close()
    # images.add_header("Logo","<logo>")
    # message.attach(images)
    message.attach('news_machine4.jpg', 'image/jpg',
                   open("appdir/static/images/background/news_machine4.jpg", 'rb').read(), 'inline',
                   headers=[['Content-ID', '<1>'], ])
    message.attach('news_machine5.jpg', 'image/png',
                   open("appdir/static/images/background/news_machine5.jpg", 'rb').read(),
                   'inline', headers=[['Content-ID', '<2>'], ])
    message.attach('logo-white.png', 'image/png', open(join("appdir/static/images", 'logo-white.png'), 'rb').read(),
                   'inline', headers=[['Content-ID', '<logo>'], ])
    message.attach('CalendarCheck.png', 'image/png',
                   open(join("appdir/static/images/icon", 'CalendarCheck.png'), 'rb').read(), 'inline',
                   headers=[['Content-ID', '<cal>']])
    message.attach(img_list[0], 'image/png',
                   open(join("appdir/static/images/blog_img", img_list[0]), 'rb').read(), 'inline',
                   headers=[['Content-ID', '<blogimg>']])

    message.html = render_template('email_template.html', adv_content=content,
                                   adv_title=title,
                                   adv_category=blog_category,
                                   adv_time=date,
                                   adv_image_route=img_list)
    # with open('appdir/static/images/logo-white.png','rb') as f:
    #     mime = MIMEBase('image', 'png', filename='logo-white.png')
    # # add required header data:
    # mime.add_header('Content-Disposition', 'attachment', filename='logo-white.png')
    # mime.add_header('X-Attachment-Id', '0')
    # mime.add_header('Content-ID', '<0>')
    # # read attachment file content into the MIMEBase object
    # mime.set_payload(f.read())
    # # encode with base64
    # encoders.encode_base64(mime)
    # # add MIMEBase object to MIMEMultipart object
    # message.attach(mime)
    try:
        mail.send(message)
    except Exception as e:
        return restful.server_error(message)
    return restful.success()


# @staff.route('/post_adv_preview', methods=['GET', 'POST'])
# def postAdv_preview():
#     img_list = ['2023033100380_3901352.jpg']
#     print(img_list)
#
#     # adv = Advs(id=final_id,
#     #            adv_content=content,
#     #            adv_title=title,
#     #            adv_category=blog_category,
#     #            adv_time=date,
#     #            adv_image_route=image)
#     # db.session.add(adv)
#     # db.session.commit()
#     # email_receive=User.query.get(email)
#
#     message = Message(subject='SANHE-Advertisement Annoucement', sender='2569787435@qq.com',
#                       recipients=['756818808@qq.com'], body="hi")
#
#     # fp = open("appdir/static/images/logo-white.png")
#     # images = MIMEImage(fp.read())
#     # fp.close()
#     # images.add_header("Logo","<logo>")
#     # message.attach(images)
#     message.attach('news_machine4.jpg', 'image/jpg',
#                    open("appdir/static/images/background/news_machine4.jpg", 'rb').read(), 'inline',
#                    headers=[['Content-ID', '<1>'], ])
#     message.attach('news_machine5.jpg', 'image/png',
#                    open("appdir/static/images/background/news_machine5.jpg", 'rb').read(),
#                    'inline', headers=[['Content-ID', '<2>'], ])
#     message.attach('logo-white.png', 'image/png', open(join("appdir/static/images", 'logo-white.png'), 'rb').read(),
#                    'inline', headers=[['Content-ID', '<logo>'], ])
#     return render_template('email_template.html', adv_content="content",
#                            adv_title="title",
#                            adv_category="blog_category",
#                            adv_time="date",
#                            adv_image_route=img_list)


@staff.route('/add_product', methods=['GET', 'POST'])
def addProduct():
    detail = request.form.get('detail')
    name = request.form.get('name').strip()
    route = func.lower(name.replace(" ", "_"))
    final_id = request.form.get('final_id')
    category = request.form.get('category')
    link = request.form.get('link')
    print(link.split(","))
    imgs = request.form.get('img_list')
    cover = imgs.split(",")[0]
    product = Products(product_id=final_id,
                       product_detail=detail,
                       product_name=name,
                       product_category=category,
                       product_route=route,
                       cover_img=cover
                       )
    db.session.add(product)
    db.session.commit()
    for i in (imgs.split(",")):
        img = Pro_Image(imgProduct_id=final_id,
                        img_path=i)
        db.session.add(img)
        db.session.commit()
    for i in (link.split(",")):
        if re.match('https://www.youtube.com', i, flags=re.I) is not None:
            # print("trueeee")
            link = Pro_Video(videoProduct_id=final_id,
                             video_path=i)
            db.session.add(link)
            db.session.commit()
    return {"id": 'success'}


@staff.route('/modify_product/<product_name>', methods=['GET', 'POST'])
@jwt_required()
def modifyProduct(product_name):
    if request.method == "GET":
        product = Products.query.filter_by(product_route=product_name).first()
        videos = Pro_Video.query.filter_by(videoProduct_id=product.product_id).all()

    if request.method == "POST":
        product = Products.query.filter_by(product_route=product_name).first()
        videos = Pro_Video.query.filter_by(videoProduct_id=product.product_id).all()
        origin_imgs = Pro_Image.query.filter_by(imgProduct_id=product.product_id).all()
        new_detail = request.form.get('detail')
        new_name = request.form.get('name').strip()
        route = func.lower(new_name.replace(" ", "_"))
        new_category = request.form.get('category')
        new_link = request.form.get('link')
        imgs = request.form.get('img_list')

        product.product_name = new_name
        product.product_detail = new_detail
        product.product_category = new_category
        product.product_route = route
        product.cover_img = imgs.split(",")[0]
        db.session.commit()

        if len(videos) != 0:
            for i in videos:
                db.session.delete(i)
                db.session.commit()
        if len(origin_imgs) != 0:
            for i in origin_imgs:
                db.session.delete(i)
                db.session.commit()
        for i in (new_link.split(",")):
            link = Pro_Video(videoProduct_id=product.product_id,
                             video_path=i)
            db.session.add(link)
            db.session.commit()
        for i in (imgs.split(",")):
            img = Pro_Image(imgProduct_id=product.product_id,
                            img_path=i)
            db.session.add(img)
            db.session.commit()

        return {"id": 'success'}

    return render_template('staff/products-modify.html', product=product, videos=videos,
                           title="Edit " + product_name)


# @staff.route('/bind_blog', methods=['GET', 'POST'])
# def bindBlog():
#
#     # id = request.form.get('final_id')
#     #
#     #
#     # db.session.add(blog)
#     db.session.commit()
#     return {"id": 'success'}


@staff.route('/newImages/<blog_id>', methods=['GET', 'POST'])
def newImages(blog_id):
    if request.method == 'POST':
        images = request.files.values()
        name = blog_id
        print("=======================")
        pic = name
        pic_dir = Config.PRODUCT_BLOG_IMG
        curtime = int(datetime.now().strftime('%H%M%S%f')[: -3])
        # num = Image.query.filter_by(imgProduct_id=product_id).count()
        print(images)
        filename = ''
        for i in images:
            print(i)
            filename = pic + '_{}.jpg'.format(curtime)
            i.save(os.path.join(pic_dir, filename))
            print(os.path.join(pic_dir, filename))
            #
            # im = cv2.imread(os.path.join(pic_dir, filename))
            # width = im.shape[0]
            # height = im.shape[1]
            # print(width)
            # print(height)
            # r = width / height
            # if r > 1:
            #     w = height
            #     wcut = int((width - w) / 2)
            #     im = im[wcut:width - wcut, 0:height]
            # elif r < 1:
            #     h = width
            #     hcut = int((height - h) / 2)
            #     im = im[0:width, hcut:height - hcut]
            # cv2.imwrite(os.path.join(pic_dir, filename), im)

            # print(os.path.exists(os.path.abspath(os.path.join(pic_dir, filename))))
            # img = Image(imgBlog_id=product_id, img_path=filename)
            # db.session.add(img)
            # db.session.commit()
        return jsonify({'name': filename})


@staff.route('/api', methods=['GET', 'POST'])
def api():
    # index of staff
    # staff_name = session.get("USERNAME")
    return render_template('staff/test.html', title="Staff Manage Blog")


@staff.route('/get_max_pro', methods=['POST'])
def get_max_pro():
    num = 4
    search = request.form.get("search")
    if search != "null":
        pro_source = Products.query.filter_by(deleteTime=None).all()
        all_pro = []
        for pro in pro_source:
            if len(Products.query.filter_by(product_category=search).all()) != 0:
                if re.match(search, pro.product_category, flags=re.I) is not None:
                    all_pro.append(pro)
            else:
                if re.search(search, pro.product_name, flags=re.I) is not None:
                    all_pro.append(pro)

    else:
        all_pro = Products.query.filter_by(deleteTime=None).all()
    a = len(all_pro) / num
    pages = int(a)
    if pages < len(all_pro) / num:
        pages = pages + 1
    return jsonify({'pages': pages, 'total_num': len(all_pro)})


@staff.route('/get_pros', methods=['POST'])
def get_pros():
    max_num = 4
    page = int(request.form.get("page"))
    search = request.form.get("search")

    print(page)
    if search != "null":
        pro_source = Products.query.filter_by(deleteTime=None).all()
        pros = []
        for pro in pro_source:
            if len(Products.query.filter_by(product_category=search).all()) != 0:
                print("category search")
                if re.match(search, pro.product_category, flags=re.I) is not None:
                    pros.append(pro)
            else:
                print("id search")
                if re.search(search, pro.product_name, flags=re.I) is not None:
                    pros.append(pro)
    else:
        pros = Products.query.filter_by(deleteTime=None).all()

    lis = []
    start_index = (page - 1) * max_num
    final_index = page * max_num
    if final_index <= len(pros):
        for e in pros[start_index:final_index]:
            lis.append(prepare_pro(e))
    else:
        for e in pros[start_index:]:
            lis.append(prepare_pro(e))
    print(lis)
    return jsonify(lis)


def prepare_pro(item):
    imgs = Pro_Image.query.filter_by(imgProduct_id=item.product_id).first()
    pro = dict()
    pro['product_id'] = item.product_id
    pro['product_poster'] = imgs.img_path
    pro['product_name'] = item.product_name
    return pro


@staff.route('/del_comment', methods=['GET', 'POST'])
def del_comment():
    id = request.form['id']
    comment = Comment.query.filter_by(id=id).first()
    if comment is not None:
        comment.fake_score = 1
        comment.audited = False
        db.session.commit()
        return jsonify({'returnValue': 200})
    else:
        return jsonify({'returnValue': 501})


@staff.route('/del_comment_real', methods=['GET', 'POST'])
def del_comment_real():
    id = request.form['id']
    comment = Comment.query.filter_by(id=id).first()
    blog = Blog.query.filter_by(id=comment.blog_id).first()
    comment_number = Comment.query.filter(and_(Comment.blog_id == int(blog.id), Comment.audited != False)).all()
    if comment.audited != False:
        blog.comment_number = len(comment_number) - 1

    db.session.delete(comment)
    db.session.commit()
    return jsonify({'returnValue': 200})


@staff.route('/pass_comment', methods=['GET', 'POST'])
def pass_comment():
    id = request.form['id']
    comment = Comment.query.filter_by(id=id).first()

    blog = Blog.query.filter_by(id=comment.blog_id).first()
    comment_number = Comment.query.filter(and_(Comment.blog_id == int(blog.id), Comment.audited != False)).all()
    blog.comment_number = len(comment_number) + 1
    if comment is not None:
        comment.fake_score = 0
        comment.audited = True
        db.session.commit()
        return jsonify({'returnValue': 200})
    else:
        return jsonify({'returnValue': 501})


@staff.route('/del_pro', methods=['GET', 'POST'])
def del_pro():
    id = request.form['id']
    product = Products.query.filter_by(product_id=id).first()
    if product is not None:
        product.deleteTime = datetime.now()
        db.session.commit()
        return jsonify({'returnValue': 200})
    else:
        return jsonify({'returnValue': 501})


@staff.route('/del_blog', methods=['GET', 'POST'])
def del_blog():
    id = request.form['id']
    blog = Blog.query.filter_by(id=id).first()
    if blog is not None:
        db.session.delete(blog)
        db.session.commit()
        return jsonify({'returnValue': 200})
    else:
        return jsonify({'returnValue': 501})
# def add_instrument(request):
#     messages = MessageModel.objects.filter(recipient=request.user, read=False).values("user").annotate(
#         time=Max("timestamp")).exclude(user=request.user).order_by("time")
#
#     users = User.objects.all()
#
#     for message in messages:
#         body = MessageModel.objects.get(user_id=message['user'], recipient=request.user, timestamp=message['time']).body
#         message['user'] = users.get(id=message['user'])
#         message['body'] = body
#
#     if request.method == "POST":
#         print(request.FILES)
#         print(request.POST)
#         f = InstrumentWithIForm(request.POST, request.FILES)
#         if f.is_valid():
#             instrument = f.save()
#             all_images = request.FILES.getlist("input24[]")
#             # print("sss", all_images, request.FILES["input24[]"])
#             # print(len(all_images))
#             for i in range(len(all_images)):
#                 # instrument.created_at = datetime.utcnow()
#                 # print(instrument.image, instrument.image1, instrument.image2, instrument.image3, instrument.image4)
#                 images = all_images[i]
#                 # print(images)
#                 if i == 0:
#                     instrument.image = images
#                 elif i == 1:
#                     instrument.image1 = images
#                 elif i == 2:
#                     instrument.image2 = images
#                 elif i == 3:
#                     instrument.image3 = images
#                 elif i == 4:
#                     instrument.image4 = images
#                 instrument.save()
#             return redirect(reverse('management:instrument_management'))
#         else:
#             return render(request, 'management_templates/add_instrument.html', {
#                 'form': f,
#                 'messages': messages,
#                 "new_order_notifications": Notification.objects.filter(is_confirm=False),
#                 "confirm_order_notifications": Notification.objects.filter(is_confirm=True),
#                 'profile': Profile.objects.filter(user=request.user.id).first(),
#             })
#     else:
#         f = InstrumentWithIForm()
#         return render(request, 'management_templates/add_instrument.html', {
#             'form': f,
#             'messages': messages,
#             "new_order_notifications": Notification.objects.filter(is_confirm=False),
#             "confirm_order_notifications": Notification.objects.filter(is_confirm=True),
#             'profile': Profile.objects.filter(user=request.user.id).first(),
#         })
