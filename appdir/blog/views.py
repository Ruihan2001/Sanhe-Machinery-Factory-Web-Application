import datetime
import json
import os
import random
import re
import sys
import time
from operator import or_

import requests
from bs4 import BeautifulSoup
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from sqlalchemy import func, and_

from appdir.blog import blog
from appdir.blog.forms import CommentForm
from appdir.blog.models import Blog, Image, Comment
from appdir import db
from appdir.sanhe import sanhe
from werkzeug.security import generate_password_hash, check_password_hash

from flask import render_template, redirect, request, url_for, session, jsonify

from appdir.sanhe.models import User


@blog.route('/index')
@jwt_required(optional=True)
def index():
    blog_show = Blog.query.all()
    print(blog_show)

    current_user_id = get_jwt_identity()
    current_user = User.query.filter_by(unionid=current_user_id).first()

    corporation_blogs = Blog.query.filter_by(blog_category='corporation').all()
    wood_blogs = Blog.query.filter_by(blog_category='wood').all()
    sharing_blogs = Blog.query.filter_by(blog_category='sharing').all()
    for blog_r in sharing_blogs:
        blog_r.blog_content = BeautifulSoup(blog_r.blog_content).get_text()
    return render_template('blog/index.html', blog_show=blog_show, cor_blogs=corporation_blogs, wood_blogs=wood_blogs,
                           shar_blogs=sharing_blogs, user=current_user, language="en")


def fake_review_detection(user_id, comment_input):
    from utils.negative_local import local_negative_word_detector
    result_array = local_negative_word_detector(comment_input)
    return result_array[0], result_array[1]


@blog.route('/blog_details/<blog_id>', methods=['GET', 'POST'])
@jwt_required(optional=True)
def details(blog_id):
    # blog_show = Blog.query.all()
    # blog = blog_show[int(id)]
    # print(blog_show)
    blog_all = Blog.query.all()
    blog_num = len(blog_all)
    blog_visited = Blog.query.filter_by(id=int(blog_id)).first()

    blog_prev = Blog.query.filter(Blog.id < int(blog_id)).all()
    if blog_prev:
        blog_prev = blog_prev[len(blog_prev) - 1]
    blog_next = Blog.query.filter(Blog.id > int(blog_id)).first()

    blogs_this_category = Blog.query.filter(
        and_(Blog.id != int(blog_id), Blog.blog_category == blog_visited.blog_category)).all()
    if len(blogs_this_category) > 2:
        blog_random = random.sample(blogs_this_category, 2)
    else:
        blog_random = []
    for blog_r in blog_random:
        blog_r.blog_content = BeautifulSoup(blog_r.blog_content).get_text()
    imgs = Image.query.filter_by(imgBlog_id=int(blog_id)).all()
    session["blog_id"] = blog_visited.id

    tags = []
    for i in blog_visited.blog_category.split(","):
        tags.append(i)

    current_user_id = get_jwt_identity()
    print("current_user_id", current_user_id, file=sys.stderr)

    comment_all = Comment.query.all()
    comment_num = len(comment_all)
    comment_form = CommentForm()

    # omit comment flagged as False
    comments = Comment.query.filter(Comment.blog_id == int(blog_id)).all()
    comment = []
    for c in comments:
        if "False" not in str(c.audited):
            comment.append(c)
    for c in comment:
        print("Comment.tetn", c.content)

    if current_user_id:
        # csrf_token = get_jwt()["csrf"]
        current_user = User.query.filter_by(unionid=current_user_id).first()
        if request.method == "POST":
            # if comment_form.validate_on_submit()
            comment_content = comment_form.comment.data
            forbid, detected_words = fake_review_detection(current_user.id, comment_content)
            if not forbid:
                com = Comment(
                    comment_author=current_user.nickname,
                    content=comment_content,
                    author_id=current_user.id,
                    blog_id=int(blog_id),
                    # code_id=1,
                    audited=False,
                    category=1,
                    fake_score=1,
                    comment_avatar_route=current_user.headimgurl,
                    comment_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
                )
                db.session.add(com)
                db.session.commit()
                return jsonify({"code": 412, "message": ",".join(detected_words)})
            else:
                try:
                    # data = {"review": comment_content}
                    # data = json.dumps(data)
                    # isFakeReview = requests.post('http://127.0.0.1:8080/review_api', data=data).text
                    isFakeReview = requests.post('http://ipa-022.ucd.ie/review_api', json={"review": comment_content})
                    print("isFakeReview", isFakeReview.json(), file=sys.stderr)
                    if isFakeReview.json()["result"] == True:
                        com = Comment(
                            comment_author=current_user.nickname,
                            content=comment_content,
                            author_id=current_user.id,
                            blog_id=int(blog_id),
                            # code_id=1,
                            category=1,
                            fake_score=1,
                            comment_avatar_route=current_user.headimgurl,
                            comment_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
                        )
                        db.session.add(com)
                        db.session.commit()
                        print('forbidden !!!!!!!!!!!!')
                        return jsonify({"code": 413, "message": "detected"})
                except Exception as e:
                    print("error", e, file=sys.stderr)
                print('add successfully!!!!!!!!!!!!')
                com = Comment(
                    comment_author=current_user.nickname,
                    content=comment_content,
                    author_id=current_user.id,
                    blog_id=int(blog_id),
                    # code_id=1,
                    category=1,
                    audited=True,
                    fake_score=0,
                    comment_avatar_route=current_user.headimgurl,
                    comment_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
                )
                db.session.add(com)
                db.session.commit()

                blog_visited.comment_number = len(comment)
                db.session.commit()
                return jsonify({"code": 200})
            # return redirect(url_for("blog.details", blog_id=blog_id))
            # return render_template('blog/blog_detail.html', blog_num=blog_num, form=comment_form, blog=blog_visited,
            #                        comment=comment, imgs=imgs, language="en", tags=tags, user=current_user,
            #                        csrf_token=csrf_token)

        else:
            return render_template('blog/blog_detail.html', blog_num=blog_num, form=comment_form, blog=blog_visited,
                                   comment=comment, imgs=imgs, language="en", tags=tags, user=current_user,
                                   blog_random=blog_random, blog_prev=blog_prev, blog_next=blog_next
                                   )

    return render_template('blog/blog_detail.html', blog_num=blog_num, form=comment_form, blog=blog_visited,
                           comment=comment, imgs=imgs, language="en", tags=tags,
                           blog_random=blog_random, blog_prev=blog_prev, blog_next=blog_next)


# @blog.route('/blog_details/<blog_id>', methods=['POST'])
# def details(blog_id):
#     # blog_show = Blog.query.all()
#     # blog = blog_show[int(id)]
#     # print(blog_show)
#     blog_all = Blog.query.all()
#     blog_num = len(blog_all)
#     blog_visited = Blog.query.filter_by(id=int(blog_id)).first()
#     imgs = Image.query.filter_by(imgBlog_id=int(blog_id))
#     session["blog_id"] = blog_visited.id
#
#     tags = []
#     for i in blog_visited.blog_category.split(","):
#         tags.append(i)
#
#     # current_user_id = get_jwt_identity()
#     # print("current_user_id", current_user_id, file=sys.stderr)
#
#     # csrf_token = get_jwt()["csrf"]
#
#     comment_all = Comment.query.all()
#     comment_num = len(comment_all)
#     comment_form = CommentForm()
#
#     comment = Comment.query.filter_by(blog_id=int(blog_id))
#
#
#     current_user = User.query.filter_by(unionid=current_user_id).first()
#
#     comment = Comment.query.filter_by(blog_id=int(blog_id))
#     # if comment_form.validate_on_submit():
#     print('add successfully!!!!!!!!!!!!')
#     com = Comment(
#         id=comment_num + 1,
#         comment_author=current_user.nickname,
#         content=comment_form.comment.data,
#         author_id=current_user.id,
#         blog_id=int(blog_id),
#         code_id=1,
#         category=1,
#         comment_avatar_route=current_user.headimgurl,
#         comment_time=time.asctime(time.localtime(time.time()))
#
#     )
#     db.session.add(com)
#     db.session.commit()
#
#     comment = Comment.query.filter_by(blog_id=int(blog_id))
#     comment_all = Comment.query.all()
#     comment_num = len(comment_all)
#     comment_form = CommentForm()
#
#     # return redirect(url_for("details", blog_id=blog_id))
#     return render_template('blog/blog_detail.html', blog_num=blog_num, form=comment_form, blog=blog_visited,
#                            comment=comment, imgs=imgs, language="en", tags=tags, user=current_user,
#                            csrf_token=csrf_token)
#
#     return render_template('blog/blog_detail.html', blog_num=blog_num, form=comment_form, blog=blog_visited,
#                            comment=comment, imgs=imgs, language="en", tags=tags, csrf_token=csrf_token)


@blog.route('/all', methods=['GET', 'POST'])
def blogs():
    blog_type = request.args.get('type')
    # filtered_blogs = Blog.query.all()
    if blog_type:
        filtered_blogs = Blog.query.filter_by(blog_category=blog_type).all()
    else:
        filtered_blogs = Blog.query.all()

    search = request.args.get('search')
    if search:
        filtered_blogs2 = []
        for blog2 in filtered_blogs:
            if search.lower() in blog2.blog_title.lower():
                filtered_blogs2.append(blog2)
        filtered_blogs = filtered_blogs2
    return render_template('blog/all_blogs.html', blogs=filtered_blogs, language="en")

# @blog.route('/all', methods=['GET', 'POST'])
# def blogs():
#     blog_type = request.args.get('type')
#     filtered_blogs = Blog.query.all()
#     # filtered_blogs = Blog.query.filter_by(blog_category=blog_type)
#     return render_template('blog/all_blogs.html', blogs=filtered_blogs, language="en")

# @blog.route('/life_style')
# def life():
#     return render_template('life-style.html', language="en")
#
# @blog.route('/travel')
# def travel():
#     return render_template('travel.html', language="en")
#
# @blog.route('/projects')
# def projects():
#     return render_template('projects.html', language="en")
#
# @blog.route('/projects_detail')
# def projects_detail():
#     return render_template('projects-detail.html', language="en")
#
# @blog.route('/price')
# def price():
#     return render_template('pricing.html', language="en")
#
# @blog.route('/team')
# def team():
#     return render_template('team.html', language="en")
#
# @blog.route('/faq')
# def faq():
#     return render_template('faq.html', language="en")
#
# @blog.route('/shop')
# def shop():
#     return render_template('shop.html', language="en")
#
# @blog.route('/shop_details')
# def shop_detail():
#     return render_template('shop-details.html', language="en")
#
# @blog.route('/contact_blog')
# def contact_blog():
#     return render_template('contact-blog.html', language="en")
#
# @blog.route('/blog_details')
# def blog_details():
#     return render_template('blog-details.html', language="en")


#
# @blog.route('/blogs')
# def blogs():
#     return render_template('blog.html', language="en")

#
# path('', index, name='index'),
# path('view/<int:post_id>', view, name='view'),
# path('post_blog', post, name='post')
#
# def index(request):
#     all_posts = Post.objects.all()
#     category_id = request.GET.get("category", None)
#     if category_id and category_id != "0":
#         all_posts = all_posts.filter(category_id=category_id)
#     # if len(posts) >= 3:
#     #     latest3Posts = posts[:3]
#     # elif len(posts) == 2:
#     #     latest3Posts = posts[:2]
#     # else:
#     #     latest3Posts = posts[:1]
#
#     paginator = Paginator(all_posts, 12, 0)
#     page = request.GET.get("page")
#     try:
#         posts = paginator.page(page)
#     except PageNotAnInteger:
#         posts = paginator.page(1)
#     except EmptyPage:
#         posts = paginator.page(paginator.num_pages)
#
#     posts.count = all_posts.count()
#
#     part_num = 3
#     p = int(page or 1)
#     if paginator.num_pages <= part_num:
#         part_pages = [i for i in range(1, paginator.num_pages + 1)]
#     elif p <= int(part_num / 2) + 1:
#         part_pages = [i for i in range(1, part_num + 1)]
#     elif p + int((part_num - 1) / 2) >= paginator.num_pages:
#         part_pages = [i for i in range(paginator.num_pages - part_num + 1, paginator.num_pages + 1)]
#     else:
#         part_pages = [i for i in range(p - int(part_num / 2), p + int((part_num - 1) / 2) + 1)]
#
#     categories = Category.objects.all()
#     category_number = {}
#     for category in categories:
#         category_number[category] = all_posts.filter(category=category).count()
#
#     return render(request, 'blog_templates/blogs.html', {
#         'index_posts': posts[:3],
#         'posts': posts,
#         'part_pages': part_pages,
#         'category_number': category_number
#         # 'latest3Posts': latest3Posts,
#     })
#
#
# def view(request, post_id):
#     post = get_object_or_404(Post, id=post_id)
#     all_comments = Comment.objects.filter(post=post)
#     paginator = Paginator(all_comments, 12, 0)
#     page = request.GET.get("page")
#     try:
#         comments = paginator.page(page)
#     except PageNotAnInteger:
#         comments = paginator.page(1)
#     except EmptyPage:
#         comments = paginator.page(paginator.num_pages)
#
#     part_num = 3
#     p = int(page or 1)
#     if paginator.num_pages <= part_num:
#         part_pages = [i for i in range(1, paginator.num_pages + 1)]
#     elif p <= int(part_num / 2) + 1:
#         part_pages = [i for i in range(1, part_num + 1)]
#     elif p + int((part_num - 1) / 2) >= paginator.num_pages:
#         part_pages = [i for i in range(paginator.num_pages - part_num + 1, paginator.num_pages + 1)]
#     else:
#         part_pages = [i for i in range(p - int(part_num / 2), p + int((part_num - 1) / 2) + 1)]
#     if request.method == 'POST':
#         if request.user.is_authenticated:
#             comment_text = request.POST.get('comment')
#             comment = Comment(body=comment_text, post=post, author=request.user)
#             comment.save()
#             return redirect(reverse('blog:view', args=(post_id,)))
#         else:
#             return redirect(reverse('accounts:log_in'))
#     return render(request, 'blog_templates/blog-details.html', {
#         'post': post,
#         'comments': comments,
#         'part_pages': part_pages,
#         'categories': Category.objects.all(),
#         'recent_posts': Post.objects.all().order_by("-created_on")[:3],
#         'similar_posts': Post.objects.filter(category_id=post.category_id)[:2]
#     })
#
# @login_required
# def post(request):
#     if request.method == "POST":
#         f = PostForm(request.POST, request.FILES)
#         if f.is_valid():
#             new_post = Post(
#                 title=f.cleaned_data['title'],
#                 body=f.cleaned_data['body'],
#                 category=f.cleaned_data['category'],
#                 main_image=f.cleaned_data['main_image'],
#                 author=request.user
#             )
#             new_post.save()
#             return redirect(reverse('blog:view', args=(new_post.id,)))
#         else:
#             return render(request, 'blog_templates/post-blogs.html', {
#                 'form': f
#             })
#         return redirect(reverse('blog:post'))
#         # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
#     else:
#         f = PostForm()
#         return render(request, 'blog_templates/post-blogs.html', {
#             'form': f
#         })
