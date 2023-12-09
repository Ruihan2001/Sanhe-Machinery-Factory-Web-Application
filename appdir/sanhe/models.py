# The purpose of this file is to build the relevant data in the database
from datetime import datetime

from appdir import db


class User(db.Model):
    __tablename__ = 'user'
    # eg: "oYml_6bLciW3UzHUPsIXVKxxgMOM"
    unionid = db.Column(db.String(128))
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # user information
    # 0-secret 1-male 2-female
    sex = db.Column(db.Integer, default=0)
    email = db.Column(db.String(128), default="")

    nickname = db.Column(db.String(128), default="", unique=True, index=True)
    password_hash = db.Column(db.String(128))
    headimgurl = db.Column(db.Integer, default="https://res.wx.qq.com/a/wx_fed/assets/res/NTI4MWU5.ico")
    # 0 - HeadOwner; 1- Product & Blog; 2- Product; 3- Blog; 9 - Customer
    permission = db.Column(db.Integer, default=9)

    adv_accept = db.Column(db.Boolean, default=True)

    # # store the course's like/collect/share user
    # children_like = db.relationship("Course", backref="like_user", secondary="user_course_like")
    # children_collect = db.relationship("Course", backref="collect_user", secondary="user_course_collect")
    # children_share = db.relationship("Course", backref="share_user", secondary="user_course_share")


# class Comment(db.Model):
#     __tablename__ = 'comment'
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     content = db.Column(db.TEXT, nullable=False)
#     # ForeignKey is the Primary key of Course, build their relationship in Table Course
#     code_id = db.Column(db.Integer, db.ForeignKey('code.id'))
#     category = db.Column(db.Integer, nullable=False)
#
#     def __repr__(self):
#         return '<Comment {}>'.format(self.content)


class Code(db.Model):
    __tablename__ = 'code'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    time = db.Column(db.DateTime, default=datetime.now)
    title = db.Column(db.TEXT, nullable=False, default="Code-1")
    # the type of this notification: like-1, collect-2, share-3, comment-4
    code = db.Column(db.TEXT, nullable=False, default="")
    score = db.Column(db.Integer, nullable=False, default=100)


class Products(db.Model):
    product_id = db.Column(db.String(32), primary_key=True)
    product_name = db.Column(db.String(20), index=True)
    product_category = db.Column(db.String(64), index=True)
    product_detail = db.Column(db.String(64))
    video_link = db.Column(db.String(64))
    deleteTime = db.Column(db.DateTime)
    cover_img = db.Column(db.String(64), default="default.png")
    product_route = db.Column(db.String(64))
    model = db.Column(db.String(64), default="")

    product_imgs = db.relationship('Pro_Image', backref='product', lazy='dynamic')
    product_videos = db.relationship('Pro_Video', backref='video_product', lazy='dynamic')

    def __repr__(self):
        return '<Products {}>'.format(self.product_name)


class Pro_Image(db.Model):
    __tablename__ = 'pro_image'
    img_id = db.Column(db.Integer, primary_key=True)
    imgProduct_id = db.Column(db.String(32), db.ForeignKey('products.product_id'))
    img_path = db.Column(db.String(64), default="default.png")

    def __repr__(self):
        return '<Image {}, {}>'.format(self.img_id, self.imgProduct_id)


# class Instrument(models.Model):
#     name = models.CharField(max_length=200, default="")
#     old_price = models.FloatField(max_length=200, default=100, validators=[
#         MinValueValidator(0.01)
#     ])
#     price = models.FloatField(max_length=200, default=100)
#     details = models.TextField(max_length=3000, default="")
#     image = models.ImageField(upload_to='uploads/instrument/image/', default='default.jpg', null=True)
#     image1 = models.ImageField(upload_to='uploads/instrument/image/', default='default.jpg', null=True)
#     image2 = models.ImageField(upload_to='uploads/instrument/image/', default='default.jpg', null=True)
#     image3 = models.ImageField(upload_to='uploads/instrument/image/', default='default.jpg', null=True)
#     image4 = models.ImageField(upload_to='uploads/instrument/image/', default='default.jpg', null=True)
#     ex_detail = models.TextField(max_length=3000, default="", null=True)
#     ad_info = models.TextField(max_length=3000, default="", null=True)
#     chinese = models.BooleanField(default=False)
#
#     # object_3d = models.FileField(upload_to='uploads/instrument/obj/', null=True, blank=True)
#     # object_mtl = models.FileField(upload_to='uploads/instrument/mtl/', null=True, blank=True)
#     object_gltf = models.FileField(upload_to='uploads/instrument/gltf/', null=True, blank=True)
#     posted_by = models.ForeignKey(User, on_delete=models.CASCADE, default=0)
#     category = models.ForeignKey("Category", null=True, blank=True, on_delete=models.CASCADE)
#     # extras = models.JSONField(null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return f'{self.name}<{self.price}>'
#
#
# class InstrumentDetail(models.Model):
#     instrument = models.OneToOneField('Instrument', on_delete=models.CASCADE)
#     details = models.TextField(null=True)
#
#
# class Category(models.Model):
#     name = models.CharField(max_length=200)
#     main_image = models.ImageField(default="default.png", upload_to='uploads/category/image/', null=True)
#     description = models.CharField(max_length=500)
#     created_at = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return f'{self.name}'

class Wishlist(db.Model):
    __tablename__ = 'wishlist'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.String(32), primary_key=True)


class Pro_Video(db.Model):
    __tablename__ = 'pro_video'
    video_id = db.Column(db.Integer, primary_key=True)
    videoProduct_id = db.Column(db.String(32), db.ForeignKey('products.product_id'))
    video_path = db.Column(db.String(64))

