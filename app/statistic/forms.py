from flask_wtf import FlaskForm
from flask_pagedown.fields import PageDownField
from wtforms import StringField, SubmitField, TextAreaField, SelectField, TimeField, DateTimeField, IntegerField, \
    HiddenField
from wtforms.validators import DataRequired, Length, ValidationError
from ..models import Channel


class NewChannelForm(FlaskForm):
    name = StringField("Название канала", validators=[DataRequired()])
    slug_name = StringField("Краткое наименование", validators=[DataRequired()])
    channel_id = StringField("ID канала", validators=[DataRequired()])
    submit = SubmitField("Сохранить")

    def validate_slug_name(self, field):
        if Channel.query.filter_by(slug_name=field.data).first():
            raise ValidationError('Придумайте другое краткое наименование')

    def validate_channel_id(self, field):
        if Channel.query.filter_by(channel_id=field.data).first():
            raise ValidationError('Канал с таким ID существует')


class RenameChannelForm(FlaskForm):
    id = HiddenField("id")
    name = StringField("Название канала", validators=[DataRequired()])
    submit = SubmitField("Сохранить")


class ContentDetailForm(FlaskForm):
    title = StringField("Заголовок", validators=[DataRequired(), Length(1, 128)])
    text_content = PageDownField(
        "Сообщение",
        validators=[DataRequired()],
        render_kw={"style": "height: 15rem", "class": "form-control"}
    )
    channel_id = SelectField("Канал", validate_choice=False, coerce=int)
    submit = SubmitField("Сохранить")


class SearchContentForm(FlaskForm):
    search = StringField(
        "Поиск",
        validators=[Length(1, 128)],
        render_kw={"class": "form-control"}

    )
    submit = SubmitField("Искать")


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
    submit = SubmitField("Сохранить")
    delete = SubmitField("Удалить")


class ContentScheduleAddForm(FlaskForm):
    datetime_pub = DateTimeField(
        "Дата и время публикации",
        validators=[DataRequired()],
        format='%d.%m.%Y %H:%M',
        render_kw={"style": "width: auto", "id": "datetime"}
    )
    submit = SubmitField('Сохранить')


class ContentScheduleDeleteForm(FlaskForm):
    id_schedule = HiddenField("id")
    datetime_pub = DateTimeField(
        "Дата и время публикации",
        format='%d.%m.%Y %H:%M',
        render_kw={"style": "width: auto", "disabled": "disabled"}
    )
    submit = SubmitField("Удалить из расписания")
