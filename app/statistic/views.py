from flask import render_template
from flask_login import current_user
from . import statistic


@statistic.route("/")
def start():
    if current_user:
        print(current_user)
    return render_template("main.html")


@statistic.route("/statistic/channels/")
def droplist_creater():
    if current_user:
        print(current_user)
    options = [
        {"value": 1, "name": "channel_1"},
        {"value": 2, "name": "channel_2"},
        {"value": 3, "name": "channel_3"},
        {"value": 4, "name": "channel_4"},
    ]
    return render_template("droplist.html", options=options)
