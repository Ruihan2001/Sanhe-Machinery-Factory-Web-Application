from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired


class CommentForm(FlaskForm):

    comment = TextAreaField(u'text_body',
                             validators=[DataRequired()],
                             render_kw={'class': 'textarea', 'rows': 8, 'cols': '45', 'maxlength':"65525",'placeholder': u'Comment'})

    submit = SubmitField('Post Comment',render_kw={'class': 'submit', 'placeholder':'Post Comment'})
