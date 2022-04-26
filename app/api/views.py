from datetime import datetime
from random import randrange
from flask import render_template, request
from flask_login import current_user, login_required
from . import api
from ..models import Channel, ChannelStatistic, ChannelContent
from .servises import add_statistic_to_answer, get_update_dict


@api.route("/statistic/channel/", methods=["GET"])
def statistic_channel_for_current_user():
    if current_user == "AnonymousUser":
        channels = Channel.query.all()[:3]
    else:
        channels = Channel.query.filter_by(author=current_user)
    answer = get_update_dict()

    for channel in channels:
        add_statistic_to_answer(answer, channel)

    return answer


@api.route("/statistic/channel/<int:id>/", methods=["GET"])
@login_required
def statistic_channel_for_id(id):
    channels = Channel.query.filter_by(id=id, author=current_user)
    answer = get_update_dict()

    for channel in channels:
        add_statistic_to_answer(answer, channel)

    return answer


@api.route("/statistic/add/", methods=["POST"])
def add_statistic():
    a = request.json
    print(Channel.quer.get(author=current_user))
    print(a)
    return {"state": "ok"}


@api.route("/test/", methods=["GET"])
def api():
    date_1 = [datetime(2012, 1, i + 1).strftime('%Y-%m-%d %H:%M:%S') for i in range(10)]
    date_2 = [datetime(2012, 1, i + 3).strftime('%Y-%m-%d %H:%M:%S') for i in range(10)]
    date_3 = [datetime(2012, 1, i + 6).strftime('%Y-%m-%d %H:%M:%S') for i in range(10)]
    answer = {
        'x2': 'x2',
        'x1': 'x1',
        'x3': 'x3',

        "xs": {
            'data1': 'x1',
            'data2': 'x2',
            'data3': 'x3',
        },
        "columns": [
            ['x1', *date_1],
            ['x2', *date_2],
            ['x3', *date_3],
            ['data1', *[i for i in range(10)]],
            ['data2', *[i for i in range(10)]],
            ['data3', *[i for i in range(10)]]
        ]
    }
    return answer
