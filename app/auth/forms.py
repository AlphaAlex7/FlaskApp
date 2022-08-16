from flask_wtf import FlaskForm
from wtforms import (
    StringField, SubmitField,
    PasswordField, BooleanField
)
from wtforms.validators import (
    DataRequired, Length,
    Regexp, EqualTo,
    ValidationError
)

from ..models import User


class LoginForm(FlaskForm):
    email = StringField(
        'Почта',
        validators=[DataRequired(), Length(1, 64)]
    )
    password = PasswordField(
        'Пароль',
        validators=[DataRequired()]
    )
    remember_me = BooleanField('Оставаться в сети')
    submit = SubmitField('Войти')


class RegistrationForm(FlaskForm):
    email = StringField(
        'Почта',
        validators=[DataRequired(), Length(1, 64)]
    )

    username = StringField(
        'Имя пользователя',
        validators=[
            DataRequired(),
            Length(1, 64),
            Regexp(
                '^[A-Za-z][A-Za-z0-9_.]*$',
                0,
                'Имя пользователя должно состоять из латинских букв и цифр'
            )
        ]
    )
    password = PasswordField(
        'Пароль',
        validators=[
            DataRequired(),
            EqualTo(
                'password2',
                message='Пароли не совпадают'
            )
        ]
    )
    password2 = PasswordField(
        'Подтвердить пароль',
        validators=[DataRequired()]
    )
    submit = SubmitField('Зарегистрироваться')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Почта уже используется')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Имя пользователя уже используется')
