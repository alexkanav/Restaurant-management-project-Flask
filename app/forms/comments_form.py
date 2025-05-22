from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length


class CommentForm(FlaskForm):
    comm_name = StringField(
        "Ваше ім'я",
        validators=[DataRequired(), Length(max=100)]
    )
    comm_text = TextAreaField(
        'Ваш відгук',
        validators=[DataRequired(), Length(max=1000)]
    )
    submit = SubmitField('Надіслати')