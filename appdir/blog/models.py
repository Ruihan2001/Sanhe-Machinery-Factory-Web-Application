from datetime import datetime
from appdir import db


class Blog(db.Model):
    __tablename__ = 'blogs'
    id = db.Column(db.Integer, primary_key=True)
    blog_title = db.Column(db.String(64), nullable=False, index=True)
    blog_description = db.Column(db.String(258))
    blog_image_route = db.Column(db.String(64))
    comment_number = db.Column(db.Integer)
    blog_time = db.Column(db.String(128))
    blog_category = db.Column(db.String(64))
    author_id = db.Column(db.Integer)
    author = db.Column(db.String(64))
    blog_content = db.Column(db.String)
    author_avatar = db.Column(db.String(64), default="../static/images/avatar/300-11.jpg")
    view_times = db.Column(db.Integer)
    deleteTime = db.Column(db.DateTime)

    blog_comment = db.relationship('Comment', backref='comment_blog', lazy='dynamic')


class Image(db.Model):
    __tablename__ = 'image'
    img_id = db.Column(db.Integer, primary_key=True)
    imgBlog_id = db.Column(db.String(32), db.ForeignKey('blogs.id'))
    img_path = db.Column(db.String(64), default="default.png")


class Comment(db.Model):
    __tablename__ = 'comment'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.TEXT)
    blog_id = db.Column(db.Integer, db.ForeignKey('blogs.id'))
    author_id = db.Column(db.Integer)
    category = db.Column(db.String)
    comment_avatar_route = db.Column(db.String(64))
    comment_author = db.Column(db.String(64))
    comment_time = db.Column(db.String)
    audited = db.Column(db.Boolean)
    fake_score = db.Column(db.Float)
    deleteTime = db.Column(db.DateTime)

#
# class Comment(models.Model):
#     author = models.ForeignKey(User, on_delete=models.CASCADE)
#     body = models.TextField()
#     created_on = models.DateTimeField(auto_now_add=True)
#     post = models.ForeignKey('Post', on_delete=models.CASCADE)
#
#     def __str__(self):
#         return self.author
#
#
# @admin.register(Comment)
# class CommentAdmin(admin.ModelAdmin):
#     list_display = ('author', 'body', 'created_on')
#
#
# class Tag(models.Model):
#     tag = models.CharField(max_length=60)
#     post = models.ForeignKey('Post', on_delete=models.CASCADE)
#
#     def __str__(self):
#         return self.tag
#
#
# @admin.register(Tag)
# class TagAdmin(admin.ModelAdmin):
#     list_display = ('tag',)
#
#
# class Category(models.Model):
#     category = models.CharField(max_length=60)
#     image = models.ImageField(default='default.jpg', upload_to='uploads/blog/image/category')
#
#     def __str__(self):
#         return self.category
#
#
# @admin.register(Category)
# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ('category',)
#
#
# # Create your models here.
# class Post(models.Model):
#     title = models.CharField(max_length=200)
#     body = models.TextField()
#     main_image = models.ImageField(default='default.jpg', upload_to='uploads/blog/image/')
#     created_on = models.DateTimeField(auto_now_add=True)
#     last_modified = models.DateTimeField(auto_now=True)
#     author = models.ForeignKey(User, on_delete=models.CASCADE)
#     category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1, related_name='posts')
#
#     def __str__(self):
#         return self.title
#
#
# @admin.register(Post)
# class PostAdmin(admin.ModelAdmin):
#     list_display = ('title', 'body', 'created_on', 'last_modified', 'category')
