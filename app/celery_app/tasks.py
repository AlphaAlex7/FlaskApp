from datetime import datetime
import time

import telebot as telebot

from . import make_celery
from .. import db
from ..models import User, ChannelContent, Channel
from app.servises.servises_schedule import content_to_pub

celery = make_celery()
bot = telebot.TeleBot('5351531243:AAEwq6LohXiwUGp3hVAXkXDC1WzqCLwsZ4c')


@celery.task
def post_processor(hours, minutes):
    regular, irregular = content_to_pub(hours=hours, minutes=minutes)
    for i in regular:
        post_task_regular.apply_async(
            (i.content_type,),
            eta=datetime.combine(datetime.now().date(), i.time_pub)
        )
    for i in irregular:
        post_task_regular.apply_async(
            (i.content.id,),
            eta=datetime.combine(i.date_pub, i.time_pub)
        )
    return f"Regular = {len(regular)}, Irregular = {len(irregular)}"


@celery.task
def post_task_regular(content_type):
    content_item = ChannelContent.query \
        .filter(ChannelContent.pub == False)
    if content_type == "NEW":
        content_item = content_item.\
            order_by(ChannelContent.date_created)
    pub_content(content_item)
    return f"Content_id = {content_item.id}"


@celery.task
def post_task_irregular(content_item_id):
    content_item = ChannelContent.query.get(content_item_id)
    pub_content(content_item)
    return f"Content_id = {content_item.id}"


def pub_content(content_item):
    channel_id = content_item.channel.channel_id
    msg = content_item.text_content
    bot.send_message(channel_id, msg)
    content_item.pub = True
    content_item.date_pub = datetime.now()
    db.session.add(content_item)
    db.session.commit()


@celery.task()
def test():
    bot.send_message(-1001512080067, "Wdawda")
    return "awd"
