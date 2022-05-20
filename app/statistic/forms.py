from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, TimeField, DateTimeField
from wtforms.validators import DataRequired, Length


class ContentDetailForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired(), Length(1, 128)])
    text_content = TextAreaField(
        'Сообщение',
        validators=[DataRequired()],
        render_kw={"style": "height: 15rem"}
    )
    channel_id = SelectField('Канал', validate_choice=False, coerce=int)
    submit = SubmitField('Сохранить')


class RegularScheduleForm(FlaskForm):
    time_pub = TimeField(
        "Время публикации",
        validators=[DataRequired()],
        render_kw={"style": "width: auto"}
    )
    content_type = SelectField(
        "Тип контента",
        render_kw={"style": "width: auto"}
    )
    submit = SubmitField('Сохранить')
    delete = SubmitField('Удалить')


class ContentScheduleAddForm(FlaskForm):
    datetime_pub = DateTimeField(
        "Дата и время публикации",
        validators=[DataRequired()],
        render_kw={"style": "width: auto"}
    )
    submit = SubmitField('Сохранить')


class ContentScheduleRemoveForm(FlaskForm):
    datetime_pub = DateTimeField(
        "Дата и время публикации",
        validators=[DataRequired()],
        render_kw={"style": "width: auto", 'disabled': 'disabled'}
    )
    submit = SubmitField('Удалить из расписания')
