# # This file is to write the route and some response to the user in different conditions
# # For some codes, I mention where I learn it when them appear first time (mainly lecture)
# import datetime
# import json
# import os
# import sys
# from flask import render_template, redirect, request, url_for, session
# # we learn how to use password protection from Slide: Flask and Databases-II
# from sqlalchemy import desc, or_
# from werkzeug.security import generate_password_hash, check_password_hash

# from appdir import app, db, Config
# from .forms import *
# from .models import Course, Comment, UserCourseLike, UserCourseCollect, UserCourseShare, Experience, Notify

# # initiate the database
# db.create_all()


# # this is used to test how base showing (mainly for navbar at the top of the website)
# @app.route('/base')
# def base():
#     if request.method == 'GET':
#         return render_template("base.html")


# # bring user to login, if he directly visit the root directory)
# @app.route('/')
# def default():
#     app.logger.info('The user accesses the root directory and goes to the login page')
#     if request.method == 'GET':
#         start_login = url_for('login', operation_type=login)
#         return redirect(start_login)


# # All user password is set to 123456 for test
# # login
# @app.route('/auth/<operation_type>', methods=['GET', 'POST'])
# def login(operation_type):
#     form_login = LoginForm()
#     form_signup = RegisterForm()
#     form_login_ad = LoginFormForAdminister()
#     move_to_login = render_template('login.html', form_login=form_login, form_login2=form_login_ad,
#                                     form_signup=form_signup)
#     redirect_to_login = url_for('login', operation_type="login")
#     if request.method == 'GET':
#         username = session.get("USERNAME")
#         if username is None:
#             return move_to_login
#         else:
#             # if the user has login in, there is item saved in session, we bring him to main course page directly
#             next_main = url_for('course_main')
#             return redirect(next_main)
#     if request.method == 'POST':
#         # when the post request is sent from user finish form for login
#         if operation_type == "login":
#             form_username = form_login.username.data
#             form_password = form_login.password.data
#             # Modify the login function to accept and validate user data (learnt it from week-5-Flask-and-WebForms.)
#             # Extra: use form_login.validate_username() to detect whether if this username has been registered
#             if form_login.validate_on_submit() and form_login.validate_username_not_exist(form_login.username):
#                 user = User.query.filter_by(username=form_username).first()
#                 if check_password_hash(user.password_hash, form_password) is False:
#                     app.logger.error("user login failed for entering wrong password")
#                     flash("wrong username or password")
#                     return redirect(redirect_to_login)
#                 # user is not None and correct password, move to main course page
#                 else:
#                     # put the login information into session
#                     # we learn how to use session from Slide: Flask and Databases-II
#                     session["USERNAME"] = user.username
#                     # set the time for the session length (default one month)
#                     if form_login.remember_me.data:
#                         session.permanent = True
#                     else:
#                         session["USERNAME"] = user.username
#                     next_main = url_for('course_main', user=user)
#                     return redirect(next_main)
#             return redirect(redirect_to_login)
#         # when the post request is sent from user finish form for register
#         elif operation_type == "signup":
#             form_username = form_signup.username.data
#             form_password = form_signup.password.data
#             # We learnt it from Lecture: week-5-Flask-and-WebForms.
#             # Extra: use form_login.validate_username() to detect whether if this username has been registered
#             if form_signup.validate_on_submit() and form_signup.validate_username_exist(form_signup.username):
#                 app.logger.info('A user Register successfully')
#                 flash("Register successfully: Your username: {}".format(form_signup.username.data))
#                 # we have use form_signup.validate_username_exist(form_signup.username) to detect the user is not exist
#                 # put user into database
#                 user = User(username=form_username, nickname=form_username,
#                             password_hash=generate_password_hash(form_password))
#                 db.session.add(user)
#                 db.session.commit()
#                 return redirect(redirect_to_login)
#         elif operation_type == "login2":
#             if form_login_ad.validate_on_submit():
#                 # when the post request is sent from administrator finish form for login
#                 form_username = form_login_ad.username.data
#                 form_password = form_login_ad.password.data
#                 user = User.query.filter_by(username=form_username, role=1).first()
#                 if user is None:
#                     return move_to_login
#                 elif check_password_hash(user.password_hash, form_password) is False:
#                     app.logger.error('Warning Administrator password')
#                     return move_to_login
#                 # user is not None and correct password, move to main course page
#                 else:
#                     app.logger.info('Administrator has login')
#                     session["ROLE"] = "Administrator"
#                     next_main = url_for('manage_database', mode_type="user", page=1)
#                     return redirect(next_main)
#         return redirect(redirect_to_login)


# # Course Main Page
# @app.route('/course/main', methods=['GET', 'POST'])
# def course_main():
#     if request.method == 'GET':
#         mode = session.get("MODE")
#         # detect whether if the session stores the information of user
#         username = session.get("USERNAME")
#         # the user's courses
#         my_courses = Course.query.filter(Course.owner == username).all()
#         # all courses includes the former
#         courses = Course.query.filter().all()
#         if username:
#             user = User.query.filter_by(username=username).first()
#         else:
#             user = None
#             # flash("You are visitor right now!")
#         return render_template('main.html', user=user, my_courses=my_courses, courses=courses, MODE=mode)


# # Create Course
# @app.route('/course/create', methods=['GET', 'POST'])
# def course_create():
#     mode = session.get("MODE")
#     username = session.get("USERNAME")
#     # if the user if visitor, jump to log in
#     if username is None:
#         # reminder user to login first
#         flash("Sorry, you have to login first if your want to create course.")
#         app.logger.warning("visitor tried to create courses, this is not allowed")
#         return redirect(url_for("login", operation_type="login"))
#     else:
#         user = User.query.filter_by(username=username).first()
#         form = CreateCourseForm()
#         # show the user's course when he in create course page
#         app.logger.info(user.username + "enter the create course page")
#         courses = Course.query.filter(Course.owner == username).all()
#         if request.method == 'GET':
#             return render_template('course_create.html', user=user, form=form, courses=courses, files="empty",
#                                    current_course=None, MODE=mode)
#         if request.method == "POST":
#             print(Course.query.all())
#             if form.validate_on_submit():
#                 title = form.title.data
#                 original_link = form.original_link.data
#                 tags = form.tags.data
#                 if tags[len(tags) - 1] == ";":
#                     tags = tags[:len(tags) - 2]
#                 description = form.description.data
#                 # connect the path which used to store the course files
#                 course_path = os.path.join(Config.RESOURCE_UPLOAD_DIR, title)
#                 os.mkdir(course_path)
#                 # two different way to build item for course table
#                 if original_link != "":
#                     # if the course is from other site
#                     course = Course(title=title, owner="forward", link=original_link, tags=tags, owner_id=user.id,
#                                     description=description)
#                 else:
#                     # if the course is original, the uploader is owner
#                     course = Course(title=title, owner=username, tags=tags, owner_id=user.id, description=description)
#                 db.session.add(course)
#                 db.session.commit()
#                 # db.session.close()
#                 f = form.cover.data
#                 extension = f.filename.split(".").pop()
#                 f.save(course_path + "\\" + "cover" + ".png")
#                 # jump to page for upload files of course
#                 return redirect(url_for('course_manage', current_course_id=course.id))
#             return render_template('course_create.html', user=user, form=form, courses=courses, current_course=None,
#                                    MODE=mode)


# # Course File Upload
# @app.route('/course/manage/<current_course_id>', methods=['GET', 'POST'])
# def course_manage(current_course_id):
#     # if the user if visitor, jump to log in
#     mode = session.get("MODE")
#     username = session.get("USERNAME")
#     if username is None:
#         return redirect(url_for("login", operation_type="login"))
#     else:
#         user = User.query.filter_by(username=username).first()
#         form = FileUploadForm()
#         current_course = Course.query.filter(Course.id == current_course_id).first()
#         if request.method == 'GET':
#             print(current_course_id, file=sys.stderr)
#             # fetch others course except from related course, store them in courses parameter
#             courses = Course.query.filter(Course.owner == username, Course.id != current_course_id).all()
#             if current_course_id == "unknown":
#                 return render_template('course_manage.html', user=user, courses=courses, current_course="unknown",
#                                        form=form, MODE=mode)
#             else:
#                 return render_template('course_manage.html', user=user, courses=courses, current_course=current_course,
#                                        course_editing=current_course, form=form, files="empty", MODE=mode)
#         if request.method == "POST":
#             # We learn how to save files from Slide: Week-8-Flask-and-databases-II.pdf
#             if form.validate_on_submit():
#                 files = form.files.data
#                 for file in files:
#                     file_name = file.filename
#                     if ".mp4" in file.filename:
#                         file_path = os.path.join(Config.RESOURCE_UPLOAD_DIR, current_course.title, file_name)
#                         file.save(file_path)
#                 return redirect(url_for('course_detail', current_course_id=current_course_id, current_video_number=1))
#         return render_template('course_manage.html', user=user, courses=None, current_course="unknown", form=form,
#                                MODE=mode)


# # Change Course
# @app.route('/course_edit/<current_course_id>', methods=['GET', 'POST'])
# def course_edit(current_course_id):
#     mode = session.get("MODE")
#     username = session.get("USERNAME")

#     current_course = Course.query.filter(Course.id == current_course_id).first()
#     # if the user if visitor, jump to log in
#     if username is None:
#         return redirect(url_for("login", operation_type="login"))
#     else:
#         user = User.query.filter_by(username=username).first()
#         form = CreateCourseForm()
#         # put the existing data into input
#         form.title.data = current_course.title
#         form.description.data = current_course.description
#         form.tags.data = current_course.tags
#         if current_course.link:
#             form.owner.data = "forward"
#             form.original_link.data = current_course.link
#         else:
#             form.owner.data = "self"
#         # show the user's course when he in create course page
#         courses = Course.query.filter(Course.owner == username).all()
#         if request.method == 'GET':
#             return render_template('course_create.html', user=user, form=form, courses=courses, files="empty",
#                                    current_course=current_course, course_editing=current_course, MODE=mode,
#                                    EDITING=True)
#         if request.method == "POST":
#             current_course.description = form.description.data
#             current_course.tags = form.tags.data
#             if current_course.link:
#                 form.owner.data = "forward"
#                 form.original_link.data = current_course.link
#             else:
#                 form.owner.data = "self"
#             db.session.commit()
#             return redirect(url_for("course_detail", current_course_id=current_course_id, current_video_number=1))
#     return redirect(url_for("course_edit", current_course_id=current_course_id))


# # Course Detail Page
# @app.route('/course/detail/<current_course_id>/<current_video_number>', methods=['GET'])
# def course_detail(current_course_id, current_video_number):
#     mode = session.get("MODE")
#     current_course = Course.query.filter(Course.id == current_course_id).first()
#     current_course_user = User.query.filter_by(id=current_course.owner_id).first()
#     # if we don't handle the text, the description will omit "\n" information, so we split them to a list
#     description_lines = current_course.description.split("\n")
#     current_course.description_lines = description_lines
#     # we also insert rank of like for current_course
#     current_course_like_rank = Course.query.filter(Course.like == current_course.like).count()
#     current_course.current_course_like_rank = current_course_like_rank
#     # if the user if visitor, don't need log in to watch course
#     username = session.get("USERNAME")
#     # show recommend courses in video detail page for user/visitor
#     courses = Course.query.filter().all()
#     # locate source directory for this course
#     files_path = os.listdir(os.path.join(Config.RESOURCE_UPLOAD_DIR, current_course.title))
#     cover_file = "cover.png"
#     files_path.remove(cover_file)
#     files = []
#     if len(files_path) == 0:
#         # if there are not videos are uploaded, move to upload
#         move_to_upload = url_for('course_manage', current_course_id=current_course.id)
#         return redirect(move_to_upload)
#     # circulate the files in the source directory
#     # package the parameters related to current_video as a object list for more easier access
#     for file_path in files_path:
#         files.append({"file_path": file_path, "file_name": file_path.replace(".mp4", "")})
#     # find the correspond video file name from files searched in source directory
#     current_video = files_path[int(current_video_number) - 1]
#     if username:
#         user = User.query.filter_by(username=username).first()
#         # experience part
#         experience_history = Experience.query.filter(Experience.user_id == user.id,
#                                                      Experience.time == datetime.date.today(),
#                                                      Experience.value == 2).first()
#         if experience_history is None:
#             experience = Experience(time=datetime.date.today(), value=1, user_id=user.id, user_name=username)
#             experience2 = Experience(time=datetime.date.today(), value=2, user_id=user.id, user_name=username)
#             db.session.add(experience)
#             db.session.add(experience2)
#             db.session.commit()

#         user_like = UserCourseLike.query.filter_by(user_id=user.id, course_id=current_course_id).first()
#         user_collect = UserCourseCollect.query.filter_by(user_id=user.id, course_id=current_course_id).first()
#         like = True if user_like else False
#         collect = True if user_collect else False
#         return render_template('course_detail.html', user=user, current_course_user=current_course_user,
#                                courses=courses, current_course=current_course, like=like, collect=collect,
#                                current_video={"path": current_video,
#                                               "name": current_video.replace(".mp4", ""),
#                                               "index": int(current_video_number), "total": len(files_path)},
#                                files=files, MODE=mode)
#     else:
#         user = None
#     # the user is not login, no need to detect the user's interaction history
#     return render_template('course_detail.html', user=user, courses=courses, current_course_user=current_course_user,
#                            current_course=current_course,
#                            current_video={"path": current_video, "name": current_video.replace(".mp4", ""),
#                                           "index": int(current_video_number), "total": len(files_path)}, files=files,
#                            MODE=mode)


# # Route for Ajax Course Interaction
# @app.route('/course/interaction/<course_id>/<page_number>/<interact_type>', methods=['POST'])
# def course_interaction(course_id, page_number, interact_type):
#     print("Course Detail Interaction:" + course_id + "; page: " + page_number + "; type:" + interact_type,
#           file=sys.stderr)
#     username = session.get("USERNAME")
#     # detect the user identity, interaction need login
#     app.logger.info("The user " + str(username) + " " + str(interact_type) + "a course")
#     if username is None:
#         flash("You have to login before making interaction.")
#     else:
#         user = User.query.filter_by(username=username).first()
#         current_course = Course.query.filter(Course.id == course_id).first()
#         # detect which kind of operation the user do (like, collect, share)
#         user_interaction = None
#         if interact_type == "like":
#             current_course.like = current_course.like + 1
#             user_interaction = UserCourseLike(page_number=page_number, user_id=user.id, course_id=course_id)
#             app.logger.info("user likeS a course")
#             target_user = User.query.filter_by(id=current_course.owner_id).first()
#             notify = Notify(type=1, user_id=user.id, target_id=target_user.id, course_id=course_id)
#             db.session.add(notify)
#             db.session.commit()
#         elif interact_type == "no-like":
#             current_course.like = current_course.like - 1
#             user_like = UserCourseLike.query.filter_by(user_id=user.id, course_id=current_course.id).first()
#             db.session.delete(user_like)
#             db.session.commit()
#             return {"message": "minus", "code": 200}
#         elif interact_type == "collect":
#             current_course.collect = current_course.collect + 1
#             user_interaction = UserCourseCollect(page_number=page_number, user_id=user.id, course_id=course_id)
#             app.logger.info("user collect a course")
#             target_user = User.query.filter_by(id=current_course.owner_id).first()
#             notify = Notify(type=2, user_id=user.id, target_id=target_user.id, course_id=course_id)
#             db.session.add(notify)
#             db.session.commit()
#         elif interact_type == "no-collect":
#             user_collect = UserCourseCollect.query.filter_by(user_id=user.id, course_id=current_course.id).first()
#             current_course.collect = current_course.collect - 1
#             db.session.delete(user_collect)
#             db.session.commit()
#             return {"message": "minus", "code": 200}
#         elif interact_type == "share":
#             app.logger.info("user share a course")
#             current_course.share = current_course.share + 1
#             user_interaction = UserCourseShare(page_number=page_number, user_id=user.id, course_id=course_id)
#             db.session.add(user_interaction)
#             db.session.commit()
#             return {"message": "minus", "code": 200}
#         # Task Part
#         if interact_type == "share":
#             experience_history = Experience.query.filter(Experience.user_id == user.id,
#                                                          Experience.time == datetime.date.today(),
#                                                          Experience.value == 4).first()
#             if experience_history is None:
#                 app.logger.info("user finish share task today")
#                 experience = Experience(time=datetime.date.today(), value=4, user_id=user.id, user_name=username)
#                 db.session.add(experience)
#         db.session.add(user_interaction)
#         db.session.commit()
#         return {"message": "add", "code": 200}
#     return {"message": "no login", "code": 404, "login": False}


# # Course Comment Fetch for AJAX
# @app.route('/course/comment_fetch/<current_course_id>/<current_page_id>/<rank_way>', methods=['GET', "POST"])
# def course_comment_fetch(current_course_id, current_page_id, rank_way):
#     if request.method == 'GET':
#         username = session.get("USERNAME")
#         # current_course = Course.query.filter(Course.id == current_course_id).first()
#         # all comment items without processing
#         raw_comment_number = Comment.query.filter(Comment.course_id == current_course_id).count()
#         raw_comments = Comment.query.filter(
#             Comment.course_id == current_course_id).order_by(Comment.time).all() if rank_way == "new" else \
#             Comment.query.filter(Comment.course_id == current_course_id).order_by(desc(Comment.like)).all()
#         # the comments that must not the head comment, save time for iterate
#         raw_comments_not_header = Comment.query.filter(Comment.reply_to.isnot(None)).all()

#         head_comments = []
#         # first fetch the head commenter
#         for comment in raw_comments:
#             from_user = User.query.filter_by(username=username).first()
#             comment.avatar = from_user.avatar
#             comment.nickname = from_user.nickname
#             if comment.reply_to is None:
#                 head_comments.append(comment)
#         comments = []
#         # second fetch the second level comments for each head commenter
#         for comment in head_comments:
#             second_comments = []
#             for raw_comment in raw_comments_not_header:
#                 if raw_comment.reply_to == comment.id:
#                     second_comments.append(raw_comment)
#             comment.second_comments = second_comments
#             comments.append(comment)
#         app.logger.info("fetch Second Layer Comment Successfully!")
#     return render_template('comment_list.html', comments=comments, user=username)


# # Ajax Course Comment
# @app.route('/course/comment/<course_id>/<page_number>', methods=['POST'])
# def course_comment(course_id, page_number):
#     print("Course Comment:" + course_id + "; page: " + page_number + "; type:",
#           file=sys.stderr)
#     username = session.get("USERNAME")
#     # detect the user identity, interaction need login
#     if username is None:
#         app.logger.warning("user is forbidden for comment before login!")
#         flash("You have to login before making interaction.")
#     else:
#         user = User.query.filter_by(username=username).first()
#         data = request.get_json()
#         if data['reply_to'] == "":
#             user_comment = Comment(user_id=user.id, user_name=user.username, content=data['content'],
#                                    course_id=course_id)
#         else:
#             user_comment = Comment(user_id=user.id, user_name=user.username, content=data['content'],
#                                    course_id=course_id, reply_to=data['reply_to'])
#         app.logger.info("user comment successfully")
#         experience_history = Experience.query.filter(Experience.user_id == user.id,
#                                                      Experience.time == datetime.date.today(),
#                                                      Experience.value == 3).first()
#         if experience_history is None:
#             experience = Experience(time=datetime.date.today(), value=3, user_id=user.id, user_name=username)
#             db.session.add(experience)
#         db.session.add(user_comment)
#         # notify part
#         current_course = Course.query.filter(Course.id == course_id).first()
#         target_user = User.query.filter_by(id=current_course.owner_id).first()
#         if target_user.id != user.id:
#             notify = Notify(type=4, user_id=user.id, target_id=target_user.id, course_id=course_id,
#                             comment_id=user_comment.id)
#             db.session.add(notify)
#         # comment_id
#         # comment_content
#         db.session.commit()
#         return {"message": "add", "code": 200}
#     return {"message": "no login", "code": 404, "login": False}


# @app.route('/course/comment/delete', methods=['POST'])
# def course_comment_delete():
#     username = session.get("USERNAME")
#     user = User.query.filter_by(username=username).first()
#     # detect the user identity, interaction need login
#     delete_id = request.form["delete_id"]
#     if username is None:
#         flash("You have to login before making interaction.")
#     else:
#         comment_delete = Comment.query.filter_by(id=delete_id).first()

#         if user.id == comment_delete.user_id:
#             db.session.delete(comment_delete)
#             db.session.commit()
#             app.logger.info("user comment is deleted")
#             return {"message": "delete", "code": 200}
#         else:
#             app.logger.warning("user can't delete other comment by mock route")
#             return {"message": "delete forbidden", "code": 404}
#     return {"message": "no login", "code": 404, "login": False}


# @app.route('/notify/delete', methods=['POST'])
# def notify_delete():
#     username = session.get("USERNAME")
#     user = User.query.filter_by(username=username).first()
#     # detect the user identity, interaction need login
#     delete_id = request.form["delete_id"]
#     if username is None:
#         flash("You have to login before making interaction.")
#     else:
#         comment_delete = Notify.query.filter_by(id=delete_id).first()
#         delete_type = comment_delete.type
#         print("Your comment has deleted!", file=sys.stderr)
#         db.session.delete(comment_delete)
#         db.session.commit()
#         return {"message": "delete", "code": 200, "type": delete_type}
#     return {"message": "no login", "code": 404, "login": False}


# # Personal Space
# @app.route('/user/space/<user_id>', methods=['GET', 'POST'])
# def user_space(user_id):
#     mode = session.get("MODE")
#     # detect the space owner is the
#     username = session.get("USERNAME")
#     user = User.query.filter_by(id=user_id).first()
#     # if the user if visitor, jump to log in
#     if username is None:
#         # reminder user to login first
#         flash("Sorry, you have to login first for looking personal space.")
#         return redirect(url_for("login", operation_type="login"))
#     else:
#         if request.method == 'GET':
#             # build a object to store the information of number for different kind of video interactions
#             number = obj = lambda: None
#             user_courses = Course.query.filter(Course.owner == user.username).all()
#             like_num = 0
#             collect_num = 0
#             comment_num = Comment.query.filter(Comment.user_id == user.id).count()
#             for course in user_courses:
#                 like_num = like_num + course.like
#                 collect_num = collect_num + course.collect
#             user.receive_like = like_num
#             user.receive_collect = collect_num
#             user.receive_comment = comment_num

#             User.query.filter(User.id == user.id).update(
#                 {'receive_like': int(like_num), 'receive_collect': int(collect_num),
#                  'receive_comment': int(comment_num)})
#             db.session.commit()
#             courses_number = Course.query.filter(Course.owner == user.username).count()
#             likes_number = UserCourseLike.query.filter(UserCourseLike.user_id == user.id).count()
#             collects_number = UserCourseCollect.query.filter(UserCourseCollect.user_id == user.id).count()
#             shares_number = UserCourseShare.query.filter(UserCourseShare.user_id == user.id).count()
#             number.courses_number = courses_number
#             number.likes_number = likes_number
#             number.collects_number = collects_number
#             number.shares_number = shares_number
#             return render_template('personal_space.html', user=user, number=number, MODE=mode)
#         if request.method == "POST":
#             print()


# # User Space Fetch for AJAX
# @app.route('/user/space/<user_id>/<page_type>', methods=['GET'])
# def user_space_fetch(user_id, page_type):
#     username = session.get("USERNAME")
#     user = User.query.filter_by(id=user_id).first()
#     title = None
#     courses = None
#     if page_type == "userCourses":
#         title = "Your Courses List" if username == user.username else "User Courses List"
#         courses = Course.query.filter_by(owner=user.username).all()
#     elif page_type == "userLikes":
#         title = "Your Recently Likes List" if username == user.username else "User Recently Likes List"
#         # join Table Query, for fetching real courses
#         courses = Course.query.join(UserCourseLike, UserCourseLike.course_id == Course.id).filter(
#             UserCourseLike.user_id == user.id).all()
#     elif page_type == "userCollects":
#         title = "Your Recently Collects List" if username == user.username else "User Recently Collects List"
#         courses = Course.query.join(UserCourseCollect, UserCourseCollect.course_id == Course.id).filter(
#             UserCourseCollect.user_id == user.id).all()
#     elif page_type == "userShares":
#         title = "Your Recently Shares List" if username == user.username else "User Recently Shares List"
#         courses = Course.query.join(UserCourseShare, UserCourseShare.course_id == Course.id).filter(
#             UserCourseShare.user_id == user.id).all()
#     return render_template('personal_space_info.html', user=user, title=title, courses=courses)


# # Personal Information
# @app.route('/user/info/<user_id>/<tab>', methods=['GET'])
# def personal_info(user_id, tab):
#     mode = session.get("MODE")
#     username = session.get("USERNAME")
#     user = User.query.filter_by(username=username).first()
#     # if the user if visitor, jump to log in
#     if username is None:
#         # reminder user to login first
#         flash("Sorry, you have to login first for looking personal information.")
#         return redirect(url_for("login", operation_type="login"))
#     else:
#         return render_template('personal_info.html', user=user, MODE=mode)


# # User Space Fetch for AJAX
# @app.route('/user/info/<user_id>/<tab>/<page_type>', methods=['GET'])
# def user_info_fetch(user_id, tab, page_type):
#     username = session.get("USERNAME")
#     user = User.query.filter_by(id=user_id).first()
#     if page_type == "mainInfo":
#         # detect whether the user finish daily tasks
#         level = 0
#         progress = 0
#         progress_hint = 0
#         progress_hint_full = 0
#         tasks_history = Experience.query.filter(Experience.user_id == user.id).count() * 5
#         if tasks_history < 20:
#             level = 1
#             progress = tasks_history / 20 * 100
#             progress_hint = tasks_history
#             progress_hint_full = 20
#         if 20 < tasks_history < 40:
#             level = 2
#             progress = tasks_history / 40 * 100
#             progress_hint = tasks_history
#             progress_hint_full = 40
#         elif 40 <= tasks_history < 80:
#             level = 3
#             progress = tasks_history / 80 * 100
#             progress_hint = tasks_history
#             progress_hint_full = 80
#         elif 80 <= tasks_history < 160:
#             level = 4
#         elif 160 <= tasks_history < 320:
#             level = 5
#         elif 320 <= tasks_history:
#             level = 6
#         tasks = Experience.query.filter(Experience.user_id == user.id, Experience.time == datetime.date.today()).all()
#         task_state = {"a": False, "b": False, "c": False, "d": False}
#         for task in tasks:
#             if task.value == 1:
#                 task_state["a"] = True
#             if task.value == 2:
#                 task_state["b"] = True
#             if task.value == 3:
#                 task_state["c"] = True
#             if task.value == 4:
#                 task_state["d"] = True
#         return render_template('personal_info_main.html', user=user, task_state=task_state, level=level,
#                                progress=progress, progress_hint=progress_hint, progress_hint_full=progress_hint_full)
#     elif page_type == "basicInfo":
#         user_gender = "gender-" + str(int(user.gender))
#         form_info = UserInfoForm(nickname=user.nickname, gender=user.gender)
#         return render_template('personal_info_edit.html', user=user, user_gender=user_gender, form=form_info)
#     elif page_type == "avatarInfo":
#         return render_template('personal_info_avatar.html', user=user, )
#     elif page_type == "userNotifyLike" or page_type == "userNotifyCollect":
#         notifies = Notify.query.filter_by(type=1).all()
#         title = "Like To My Course" if page_type == "userNotifyLike" else "Collect To My Course"
#         for notify in notifies:
#             course = Course.query.filter_by(id=notify.course_id).first()
#             if course is not None:
#                 notify.course_title = course.title
#                 notify.course_total_like = course.like
#             from_user = User.query.filter_by(id=notify.user_id).first()
#             notify.from_name = from_user.nickname
#             notify.from_avatar = from_user.avatar
#         return render_template('personal_info_notification.html', title=title, user=user, notifies=notifies)
#     elif page_type == "userNotifyComment":
#         notifies = Notify.query.filter_by().all()
#         for notify in notifies:
#             course = Course.query.filter_by(id=notify.course_id).first()
#             if course is not None:
#                 notify.course_title = course.title
#             from_user = User.query.filter_by(id=notify.user_id).first()
#             notify.from_name = from_user.nickname
#             notify.from_avatar = from_user.avatar
#             raw_comment = Comment.query.filter(Comment.id == notify.comment_id).first()
#             if raw_comment is not None:
#                 notify.from_comment_content = raw_comment.content
#     return render_template('personal_info_notification.html', title="Comment To Me", user=user, notifies=notifies,
#                            type_information="leave a Comment under my course")


# @app.route('/change/avatar', methods=['POST'])
# def changeAvatar():
#     username = session.get("USERNAME")
#     user = User.query.filter_by(username=username).first()
#     user.avatar = request.form["avatar_id"]
#     app.logger.info(username + " changed his avatar as " + str(user.avatar))
#     print("You have changed avatar!" + user.avatar, file=sys.stderr)
#     db.session.commit()
#     return {"code": 200, "message": "avatar changed"}


# @app.route('/change/user/info', methods=['POST'])
# def changeUserInfo():
#     username = session.get("USERNAME")
#     user = User.query.filter_by(username=username).first()
#     form_info = UserInfoForm()
#     if form_info.validate_on_submit():
#         # print("You have changed avatar!" + user.avatar, file=sys.stderr)
#         user.nickname = form_info.nickname.data
#         user.gender = form_info.gender.data
#         user.description = form_info.description.data
#         db.session.commit()
#         app.logger.info("change User info Success")
#         return redirect(url_for("personal_info", user_id=user.id, tab="main"))
#     app.logger.error("change User info Failed")
#     return redirect(url_for("personal_info", user_id=user.id, tab="info"))
#     # return redirect(url_for("personal_info", user_id=user.id, tab="main"))


# @app.route('/mode/<mode_type>', methods=['GET'])
# def change_mode(mode_type):
#     session["MODE"] = "DARK" if mode_type == "dark" else "MOON"
#     return {"message": "ok", "code": 200}


# @app.route('/course/search/<rank_way>', methods=['GET', 'POST'])
# def search_course(rank_way):
#     username = session.get("USERNAME")
#     user = None
#     if username:
#         user = User.query.filter_by(username=username).first()
#     else:
#         app.logger.info("visitor is skimming the search page")
#     mode = session.get("MODE")
#     form = QueryForm()
#     if request.method == 'GET':
#         return render_template("course_search.html", form=form, MODE=mode, user=user)
#     elif request.method == "POST":
#         keyword = request.form['keyword']
#         courses = Course.query.filter(or_(Course.title.like("%" + keyword + "%"),
#                                           Course.tags.like("%" + keyword + "%"))) \
#             .order_by(Course.time).all() if rank_way == "new" else \
#             Course.query.filter(or_(Course.title.like("%" + keyword + "%"),
#                                     Course.tags.like("%" + keyword + "%"))).order_by(desc(Course.like)).all()
#         for course in courses:
#             course.owner_user = User.query.filter_by(id=course.owner_id).first().nickname
#         return render_template("course_search_result.html", form=form, courses=courses, MODE=mode, user=user)
#     return render_template("course_search_result.html", form=form, MODE=mode, user=user)


# # Log out when user want to login again
# @app.route('/logout', methods=['GET'])
# def logout():
#     # we learn how to remove session from Slide: Flask and Databases-II
#     session.pop("USERNAME", None)
#     # session.clear()
#     back_main = url_for('course_main')
#     return redirect(back_main)


# # Log out when user has entered the main menu
# @app.route('/main/logout', methods=['GET'])
# def logout_to_main():
#     app.logger.info("User has logout!")
#     session.pop("USERNAME", None)
#     # session.clear()
#     back_main = url_for('course_main')
#     return redirect(back_main)


# # (from second input way)
# # Username: Administrator
# # Password: 123456
# # This is the UI for remove all records in database
# @app.route('/administrator/<mode_type>/<int:page>', methods=['GET'])
# def manage_database(mode_type, page):
#     mode = session.get("MODE")
#     if request.method == 'GET':
#         # page = int(request.args.get('page', 1))
#         # the page index
#         # item number for each page
#         page_num = int(request.args.get('page_num', 10))
#         # fetch data from database
#         if mode_type == 'user':
#             paginate = User.query.order_by('id').paginate(page, page_num)
#             users = paginate.items
#             for user in users:
#                 user.password_hash = "secret"
#             return render_template('Administrator.html', items=users, paginate=paginate, mode=mode_type, MODE=mode)
#         elif mode_type == 'course':
#             paginate = Course.query.order_by('id').paginate(page, page_num)
#             courses = paginate.items
#             return render_template('Administrator.html', items=courses, paginate=paginate, mode=mode_type, MODE=mode)
#         elif mode_type == "experience":
#             paginate = Experience.query.order_by('id').paginate(page, page_num)
#             experiences = paginate.items
#             return render_template('Administrator.html', items=experiences, paginate=paginate, mode=mode_type,
#                                    MODE=mode)
#         elif mode_type == "notify":
#             paginate = Notify.query.order_by('id').paginate(page, page_num)
#             notifies = paginate.items
#             return render_template('Administrator.html', items=notifies, paginate=paginate, mode=mode_type, MODE=mode)
#         elif mode_type == "comment":
#             paginate = Comment.query.order_by('id').paginate(page, page_num)
#             comments = paginate.items
#             return render_template('Administrator.html', items=comments, paginate=paginate, mode=mode_type, MODE=mode)
#         elif mode_type == "user_course_collect":
#             paginate = UserCourseCollect.query.order_by('id').paginate(page, page_num)
#             user_collects = paginate.items
#             return render_template('Administrator.html', items=user_collects, paginate=paginate, mode=mode_type,
#                                    MODE=mode)
#         elif mode_type == "user_course_like":
#             paginate = UserCourseLike.query.order_by('id').paginate(page, page_num)
#             user_likes = paginate.items
#             return render_template('Administrator.html', items=user_likes, paginate=paginate, mode=mode_type, MODE=mode)
#         elif mode_type == "user_course_share":
#             paginate = UserCourseShare.query.order_by('id').paginate(page, page_num)
#             user_shares = paginate.items
#             return render_template('Administrator.html', items=user_shares, paginate=paginate, mode=mode_type,
#                                    MODE=mode)


# @app.route('/administrator/<mode_type>/<int:page>/remove', methods=['POST'])
# def remove_from_database(mode_type, page):
#     app.logger.warning("Administrator is removing record of the database. Table: " + mode_type)
#     user_identify = session.get("ROLE")
#     if user_identify == "Administrator":
#         # detect the user identity, interaction need login
#         delete_id = request.form["delete_id"]
#         if mode_type == "user":
#             delete_item = User.query.filter_by(id=delete_id).first()
#         elif mode_type == "course":
#             delete_item = Course.query.filter_by(id=delete_id).first()
#         elif mode_type == "experience":
#             delete_item = Experience.query.filter_by(id=delete_id).first()
#         elif mode_type == "notify":
#             delete_item = Notify.query.filter_by(id=delete_id).first()
#         elif mode_type == "comment":
#             delete_item = Comment.query.filter_by(id=delete_id).first()
#         elif mode_type == "user_course_collect":
#             delete_item = UserCourseCollect.query.filter_by(id=delete_id).first()
#         elif mode_type == "user_course_like":
#             delete_item = UserCourseLike.query.filter_by(id=delete_id).first()
#         elif mode_type == "user_course_share":
#             delete_item = UserCourseShare.query.filter_by(id=delete_id).first()
#         # print("Your comment has deleted!", file=sys.stderr)
#         db.session.delete(delete_item)
#         db.session.commit()
#         return {"message": "delete success", "code": 200}
#     return {"message": "failed", "code": 404, "login": False}


# @app.route('/validator/title/check_exist', methods=['POST'])
# def check_title_exist():
#     user_identify = session.get("ROLE")
