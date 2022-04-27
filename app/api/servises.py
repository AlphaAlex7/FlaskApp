import datetime
from typing import Union

from flask_sqlalchemy import BaseQuery
from ..models import ChannelStatistic, Channel, User, AnonymousUser


def get_channels_for_user(current_user: Union[User, AnonymousUser]) -> BaseQuery:
    if current_user == "AnonymousUser":
        return Channel.query.all()[:3]
    else:
        return Channel.query.filter_by(author=current_user)


def add_statistic_to_answer(answer: dict, channel: Channel, days_delta: int = 20) -> None:
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


def get_update_dict() -> dict:
    return {"xs": {}, "columns": [], }
