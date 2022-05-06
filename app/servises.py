import datetime
from typing import Union

from flask_sqlalchemy import BaseQuery
from .models import ChannelStatistic, Channel, User, AnonymousUser, ChannelContent


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
    stat = ChannelStatistic.query.filter(
        ChannelStatistic.channel_id == channel.id).order_by(ChannelStatistic.date)[-11:]

    new_stat = []
    for i, e in enumerate(stat[:-1]):
        new_stat.append(stat[i + 1].followers - e.followers)
    answer["colors"][channel.slug_name] = get_color_for_graf(channel.id)
    answer["columns"].append([
        channel.slug_name,
        sum(new_stat) / len(new_stat)
    ])


def add_average_content_views_statistic_to_answer(answer: dict, channel: Channel) -> None:
    stat = ChannelContent.query.filter(
        ChannelContent.channel == channel,
        ChannelContent.pub == True).order_by(ChannelContent.date_pub)[-11:]

    answer["colors"][channel.slug_name] = get_color_for_graf(channel.id)
    answer["columns"].append([
        channel.slug_name,
        sum((i.number_of_views for i in stat)) / len(stat)
    ])


def get_content_for_chanel(current_user, id, page):
    channel = get_channels_for_user(current_user, id=id).first()
    content = ChannelContent.query.filter(
        ChannelContent.channel_id == channel.id).paginate(page, 10, False).items
    return content


def get_table_context(content):
    table_head = [{"name": i} for i in ["title", "date_created", "date_pub", "number_of_views", "pub"]]
    table_row = [{"name": element.id,
                  "value": [element.title, element.date_created, element.date_pub, element.number_of_views,
                            element.pub]} for element in content]
    return table_head, table_row


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


def get_update_dict() -> dict:
    return {"xs": {}, "columns": [], "colors": {}}
