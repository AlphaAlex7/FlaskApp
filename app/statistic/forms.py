from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, DateTimeField
from wtforms.validators import DataRequired, Length, Regexp, EqualTo, ValidationError

from ..models import ChannelContent


class ContentDetailForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired(), Length(1, 128)])
    text_content = TextAreaField(
        'Сообщение',
        validators=[DataRequired()],
        render_kw={"style": "height: 15rem"}
    )
    channel_id = SelectField('Канал', validate_choice=False, coerce=int)
    submit = SubmitField('Сохранить')
