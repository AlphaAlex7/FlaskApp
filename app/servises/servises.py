import datetime
import re
from typing import Union

from flask import url_for, flash
from flask_sqlalchemy import BaseQuery, Pagination
from sqlalchemy import desc

from .. import db
from ..models import(
    ChannelStatistic, Channel,
    User, AnonymousUser,
    ChannelContent, ScheduleContent,
    ScheduleRegular
)
from .form_helper import form_to_model
from .enum_helpers import FlashType


def rename_channel(id_channel, form):
    channel = Channel.query.get(id_channel)

    flash_message = f"Канал {channel.name} был переименован на {form.name.data}"

    form_to_model(form, channel)
    db.session.add(channel)
    db.session.commit()
    flash(flash_message, FlashType.SUCCESS.value)


def create_channel(current_user, form):
    channel = Channel()
    if current_user == "AnonymousUser":
        channel.author_id = User.query.filter_by(username="ieshua").first().id
    else:
        channel.author_id = current_user.id

    form_to_model(form, channel)
    db.session.add(channel)
    sstatistic = ChannelStatistic(channel=channel, followers=0)
    db.session.add(sstatistic)
    db.session.commit()
    flash(f"Канал, {channel.name}, добавлен.", FlashType.SUCCESS.value)


def get_channels_for_user(current_user: Union[User, AnonymousUser], id: int = None) -> BaseQuery:
    if current_user == "AnonymousUser":
        current_user = User.query.filter_by(username="ieshua").first()
    return get_channels(user=current_user, id=id)


def get_channels(user: User, id: int = None):
    query_set = Channel.query.filter_by(author=user)
    if id:
        query_set = query_set.filter(Channel.id == id)
    return query_set


def add_main_statistic_to_answer(answer: dict, channel: Channel, days_delta: int = 20) -> None:
    stat = ChannelStatistic.query.filter(
        ChannelStatistic.channel_id == channel.id,
        ChannelStatistic.date > (datetime.datetime.now() - datetime.timedelta(days=days_delta))
    ).all()

    answer["colors"][channel.slug_name] = get_color_for_graf(channel.id)
    answer[f"x_{channel.slug_name}"] = f"x_{channel.slug_name}"
    answer["xs"][channel.slug_name] = f"x_{channel.slug_name}"
    answer["columns"].append([
        channel.slug_name,
        *[i.followers for i in stat]
    ])
    answer["columns"].append([
        f"x_{channel.slug_name}",
        *[i.date.strftime('%Y-%m-%d %H:%M:%S') for i in stat]
    ])


def get_color_for_graf(id):
    colors = ['#B22222', '#0000ff', '#ADFF2F', '#FFD700', "#ADD8E6", "#0d6efd",
              "#6610f2", "#6f42c1", "#d63384", "#dc3545", "#fd7e14", "#ffc107",
              "#198754", "#20c997", "#0dcaf0", "#ffffff", "#6c757d", "#343a40",
              "#f8f9fa", "#e9ecef", "#dee2e6", "#ced4da", "#adb5bd", "#6c757d",
              "#495057", "#343a40", "#212529", "#0d6efd", "#6c757d", "#198754",
              "#0dcaf0", "#ffc107", "#dc3545", "#f8f9fa"]

    return colors[id % len(colors)]


def add_average_subscribers_statistic_to_answer(answer: dict, channel: Channel) -> None:
    stat = ChannelStatistic.query \
               .filter(ChannelStatistic.channel_id == channel.id) \
               .order_by(ChannelStatistic.date)[-11:]

    new_stat = []
    for i, e in enumerate(stat[:-1]):
        new_stat.append(stat[i + 1].followers - e.followers)

    answer["colors"][channel.slug_name] = get_color_for_graf(channel.id)
    if len(new_stat):
        answer["columns"].append([
            channel.slug_name,
            sum(new_stat) / len(new_stat)
        ])
    else:
        answer["columns"].append([
            channel.slug_name,
            0
        ])


def add_average_content_views_statistic_to_answer(answer: dict, channel: Channel) -> None:
    stat = ChannelContent.query.filter(
        ChannelContent.channel == channel,
        ChannelContent.pub == True).order_by(ChannelContent.date_pub)[-11:]

    answer["colors"][channel.slug_name] = get_color_for_graf(channel.id)
    if len(stat):
        answer["columns"].append([
            channel.slug_name,
            sum((i.number_of_views for i in stat)) / len(stat)
        ])
    else:
        answer["columns"].append([
            channel.slug_name,
            0
        ])


def get_content_for_chanel(current_user, id: int, page: int, sorting: str, search: str) -> Pagination:
    channel = get_channels_for_user(current_user, id=id).first()

    content = ChannelContent.query \
        .filter(*content_searching(channel, search)) \
        .order_by(*content_sort_order(sorting)) \
        .paginate(page, 20, False)

    return content


def content_searching(channel: Channel, search: str):
    if search:
        return ChannelContent.channel_id == channel.id, ChannelContent.title.like(f"%{search}%")
    else:
        return (ChannelContent.channel_id == channel.id,)


def content_sort_order(sorting: str) -> tuple:
    sort_field = re.sub(r"(_asc|_desc)", "", sorting)

    if sort_field != "title":
        if sorting.endswith("_asc"):
            return ChannelContent.__dict__[sort_field], ChannelContent.title
        else:
            return desc(ChannelContent.__dict__[sort_field]), ChannelContent.title
    else:
        if sorting.endswith("_asc"):
            return (ChannelContent.title,)
        else:
            return (desc(ChannelContent.title),)


def get_regular_schedule(channel, page):
    return ScheduleRegular.query \
        .filter(ScheduleRegular.channel_id == channel.id) \
        .order_by(ScheduleRegular.time_pub) \
        .paginate(page, 20, False)


def get_content_schedule(channel, page):
    return ScheduleContent.query \
        .filter(ScheduleContent.channel_id == channel.id) \
        .order_by(ScheduleContent.date_pub,ScheduleContent.time_pub) \
        .paginate(page, 20, False)


def get_option_sort_content(id):
    url_prefix = url_for("statistic.content", id=id) + "?sorting="
    return [
        {"href": url_prefix + "title_asc", "name": "по названию (от A до Z)"},
        {"href": url_prefix + "title_desc", "name": "по названию (от Z до A)"},
        # {"href": url_prefix + "date_created_asc", "name": "по дате создания"},
        {"href": url_prefix + "date_created_desc", "name": "по дате создания (сначала новые)"},
        # {"href": url_prefix + "date_pub_asc", "name": "по дате публикации"},
        {"href": url_prefix + "date_pub_desc", "name": "по дате публикации (сначала новые)"},
        # {"href": url_prefix + "number_of_views_asc", "name": "по названию (от Z до A)"},
        {"href": url_prefix + "number_of_views_desc", "name": "по количеству просмотров (по убыванию)"},
        {"href": url_prefix + "pub_asc", "name": "сначала не опубликованные"},
        {"href": url_prefix + "pub_desc", "name": "сначала опубликованные"},
    ]


def get_channels_for_menu(channels):
    return [
        {"value": channel.id, "name": channel.name, "color": get_color_for_graf(channel.id)}
        for channel in channels
    ]


def get_date_for_filter():
    return [
        {"value": i, "name": "за " + str(i) + " дней"}
        for i in [20, 60, 90]
    ]
