import datetime
from typing import Union

from flask_sqlalchemy import BaseQuery
from .models import ChannelStatistic, Channel, User, AnonymousUser


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


def add_average_subscribers_statistic_to_answer(answer: dict, channel: Channel) -> None:
    stat = ChannelStatistic.query.filter(
        ChannelStatistic.channel_id == channel.id).order_by(ChannelStatistic.date)[-6:]
    print(stat)
    new_stat = []
    for i, e in enumerate(stat[:-1]):
        new_stat.append(stat[i+1].followers - e.followers)

    # answer[f"x_{channel.slug_name}"] = f"x_{channel.slug_name}"
    # answer["xs"][channel.slug_name] = f"x_{channel.slug_name}"
    answer["columns"].append([
        channel.slug_name,
        *new_stat
    ])
    # answer["columns"].append([
    #     f"x_{channel.slug_name}",
    #     *[i.date.strftime('%Y-%m-%d %H:%M:%S') for i in stat]
    # ])

def get_date_for_filter():
    return [
        {"value": i, "name": i}
        for i in [20, 60, 90]
    ]


def get_update_dict() -> dict:
    return {"xs": {}, "columns": [], }
