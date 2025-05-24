from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo


class RegisterForm(FlaskForm):
    username = StringField("Ім'я", validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email(message="Некоректна поштова скринька.")])
    password = PasswordField("Пароль", validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField(
        "Підтвердіть пароль",
        validators=[
            DataRequired(),
            EqualTo('password', message="Паролі не збігаються!")
        ]
    )
    submit = SubmitField('Зареєструвати')
