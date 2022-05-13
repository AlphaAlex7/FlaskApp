from datetime import datetime
from flask import render_template, request
from flask_login import current_user
from . import api
from ..models import Channel
from ..servises import get_channels_for_user


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
