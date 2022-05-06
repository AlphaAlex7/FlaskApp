from datetime import datetime
from flask import render_template, request
from flask_login import current_user, login_required
from . import api
from ..models import Channel
from ..servises import add_main_statistic_to_answer, get_update_dict, get_channels_for_user, \
    add_average_subscribers_statistic_to_answer


@api.route("/statistic/channel-main-chart/", methods=["GET"])
def statistic_channel_for_current_user():
    channels = get_channels_for_user(current_user, id=request.args.get("channel_id"))
    answer = get_update_dict()
    for channel in channels:
        add_main_statistic_to_answer(answer, channel, days_delta=int(request.args.get("days_delta", 20)))
    return answer


@api.route("/statistic/channel-average-subscribers/", methods=["GET"])
def average_subscribers_channel_for_current_user():
    channels = get_channels_for_user(current_user, id=request.args.get("channel_id"))
    answer = get_update_dict()
    for channel in channels:
        add_average_subscribers_statistic_to_answer(answer, channel)
    answer["columns"].sort(key=lambda x: x[1])
    return answer


@api.route("/statistic/channels_droplist/", methods=["GET"])
def droplist_creater():
    channels = get_channels_for_user(current_user)
    options = [
        {"value": channel.id, "name": channel.name}
        for channel in channels
    ]
    return render_template("dashboard/droplist.html", title="Все каналы", options=options)


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
