# import sys
# from flask import flash
# from flask_wtf import FlaskForm
# from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, RadioField, FileField, \
#     MultipleFileField
# # from flask_wtf.file import FileField
# from wtforms.validators import DataRequired, ValidationError, Regexp, Length
# from flask_wtf.file import FileAllowed
#
# from appdir.base.models import User
#
#
# class LoginForm(FlaskForm):
#     username = StringField('USERNAME',
#                            validators=[DataRequired(message='required: username can\'t be empty'),
#                                        Regexp(message=u'Invalid Username',
#                                               regex="^[A-Za-z0-9]{6,60}$")],
#                            render_kw={'class': 'username_l', "id": "username_l"})
#     password = PasswordField('PASSWORD', validators=[DataRequired(message=u'password can\'t be empty'),
#                                                      Regexp(message=u'Invalid Username',
#                                                             regex="^[A-Za-z0-9]{6,60}$")],
#                              render_kw={'class': 'password_l', "id": "password_l"})
#     remember_me = BooleanField('Remember Me')
#
#     # validate whether if the username has been register
#     def validate_username_not_exist(self, field):
#         if User.query.filter_by(username=field.data).first() is None:
#             flash(u'Sorry, this username has not be registered.')
#             return False
#             # raise ValidationError(u'Sorry, this username has not be registered.')
#         else:
#             return True
#
#
# # Form for Administer to Log in (username, password)
# # We use submit button instead of input[type="submit"], so we didn't add submit here
# class LoginFormForAdminister(FlaskForm):
#     username = StringField('USERNAME', validators=[DataRequired(message=u'username can\'t be empty')],
#                            render_kw={'class': 'username_l2', "id": "username_l2"})
#     password = PasswordField('PASSWORD', validators=[DataRequired(message=u'password can\'t be empty')],
#                              render_kw={'class': 'password_l2', "id": "password_l2"})
#
#
# # Form for User to Register in (username, password)
# # twice password validator written by javascript (in file login.js)
# # We use submit button instead of input[type="submit"], so we didn't add submit here
# class RegisterForm(FlaskForm):
#     username = StringField('USERNAME', validators=[DataRequired(message=u'username can\'t be empty'),
#                                                    Regexp(message=u'Invalid Username',
#                                                           regex="^[A-Za-z0-9]{6,60}$")
#                                                    ],
#                            render_kw={'class': 'username_r', "id": "username_r"})
#     password = PasswordField('PASSWORD', validators=[DataRequired(message=u'password can\'t be empty'),
#                                                      Regexp(message=u'Invalid Password',
#                                                             regex="^[A-Za-z0-9]{6,60}$")],
#                              render_kw={'class': 'password_r', "id": "password_r"})
#
#     # For the twice input for the password, we use js instead of Equal To
#     # validate whether if the username has register
#     def validate_username_exist(self, field):
#         if User.query.filter_by(username=field.data).first():
#             flash(u'Sorry, this username has been registered.')
#             return False
#             # raise ValidationError(u'Sorry, this username has been registered.')
#         else:
#             return True
#
#
# # Form for user to Create a course (cover, title, owner, original_link, tags, description, submit)
# class CreateCourseForm(FlaskForm):
#     cover = FileField('Cover', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif'])],
#                       render_kw={'class': 'input-img', "onchange": "showCover(this)"})
#
#     title = StringField('Title', validators=[DataRequired(),
#                                              Regexp(message=u'Invalid Title (characters and number only, 5-40 words)',
#                                                     regex="^[A-Za-z0-9\s]{5,100}$")],
#                         render_kw={'class': 'input-box-title',
#                                    'placeholder': u'Please enter a title for the course (5-100 words)'})
#     owner = RadioField("Owner", choices=[('self', 'self'),
#                                          ('forward', 'forward')], validators=[DataRequired()],
#                        render_kw={'class': 'input-box-owner', "onclick": "checkSelected()"})
#     original_link = StringField('Forward',
#                                 validators=[],
#                                 render_kw={'class': 'input-box-link',
#                                            "style": "display:none",
#                                            'placeholder': u'Please enter the link that the course can be found ('
#                                                           u'optional)'})
#     tags = StringField('Tags', validators=[DataRequired()], render_kw={'class': 'input-box-tags',
#                                                                        "id": "input-box-tags",
#                                                                        "value": "", "onblur": "DisActive()",
#                                                                        "onfocus": "Active()"})
#     description = TextAreaField('Description',
#                                 validators=[DataRequired(),
#                                             Length(min=1, max=600, message=u'Description should less than 20')],
#                                 render_kw={'class': 'input-box-description',
#                                            'placeholder': u'Please write some descriptions to introduce it 😃 (no '
#                                                           u'more that 600 words)'})
#
#     submit = SubmitField('Submit', render_kw={'class': 'input-submit', 'value': 'Ensure to Create'})
#     # for change submit
#     submit2 = SubmitField('Submit', render_kw={'class': 'input-submit', 'value': 'Ensure to Change'})
#
#     # validate whether if the username has register
#
#     def validate_tags_exist(self, field):
#         if User.query.filter_by(username=field.data).first():
#             flash(u'Why not add tags for other easier to find it?')
#             return False
#             # raise ValidationError(u'Sorry, this username has been registered.')
#         else:
#             return True
#
#
# # Form for user to Upload files for a course (files, submit)
# class FileUploadForm(FlaskForm):
#     files = MultipleFileField('Cover', validators=[DataRequired(), FileAllowed(["mp4"],
#                                                                                message=u'Please add video with format x.mp4')],
#                               render_kw={"id": "trigger-for-upload", "style": "display:none"})
#     files_click = MultipleFileField('Cover',
#                                     validators=[DataRequired(), FileAllowed(["mp4"],
#                                                                             message=u'Please add video with format x.mp4')],
#                                     render_kw={"id": "trigger-for-upload-by-click", "style": "display:none"})
#     submit = SubmitField('Submit', render_kw={'class': 'input-submit-upload', 'value': 'Ensure to Upload'})
#
#
# # Form for user to change their infoS
# class UserInfoForm(FlaskForm):
#     nickname = TextAreaField('Nickname', validators=[DataRequired(), Regexp(
#         message=u'Invalid Nickname (6-60 words without special character)',
#         regex="^[A-Za-z0-9]{6,60}$")],
#                              render_kw={"class": "user-info-form-input-box", "rows": "2",
#                                         "placeholder": "Your Nickname"})
#
#     description = TextAreaField('My Description', validators=[Regexp(message=u'Invalid length (should less than 500)',
#                                                                      regex="^.{0,500}$")],
#                                 render_kw={"class": "form-textarea-box", "rows": "2",
#                                            "placeholder": u'Introduce yourself to others - ( ゜- ゜)つロ'})
#     gender = RadioField("Gender", choices=[(0, "secret"), (1, "male"), (2, "female")],
#                         validators=[DataRequired()],
#                         render_kw={'class': 'gender-radio'})
#     submit = SubmitField('Submit', render_kw={'class': 'el-button el-button-save', 'value': 'SAVE'})
#
#
# # Form for user to change their infoS
# class QueryForm(FlaskForm):
#     keyword = StringField('Search Keyword',
#                           validators=[DataRequired(),
#                                       Length(min=1, max=20, message=u'Search Keyword should less than 20'),
#                                       Regexp(message=u'Invalid Username',
#                                              regex="^[A-Za-z0-9]{1,60}$"), ],
#                           render_kw={"class": "search-keyword",
#                                      "placeholder": u'Please enter Search Keyword'})
#     submit = StringField('Submit', render_kw={"type": "button", 'class': 'search-button', 'value': 'Search',
#                                               "onclick": "Search()"})
