import datetime
import time
from . import make_celery
from .. import db
from ..models import User, ChannelContent, Channel
from ..servises import get_channels_for_user

celery = make_celery()


@celery.task()
def task_1():
    user = User.query.filter_by(username="ieshua").first()
    channel = get_channels_for_user(user)[0]
    res = ChannelContent(
        title=f"test_{datetime.datetime.now().time()}",
        text_content=f"{'0'*1000}",
        channel_id=channel.id
    )
    db.session.add(res)
    db.session.commit()
