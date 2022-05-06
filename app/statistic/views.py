from flask import render_template, request, redirect, url_for
from flask_login import current_user
from . import statistic
from ..servises import get_channels_for_user, get_date_for_filter, get_color_for_graf


@statistic.route("/")
def start():
    return redirect(url_for("statistic.subscribe"))


@statistic.route("/subscribe/")
def subscribe():
    channels = get_channels_for_user(current_user)
    option_channel = [
        {"value": channel.id, "name": channel.name, "color": get_color_for_graf(channel.id)}
        for channel in channels
    ]
    option_date = get_date_for_filter()
    return render_template(
        "dashboard/statistic_subscribe.html",
        path_url="subscribe",
        option_channel=option_channel,
        option_date=option_date
    )


@statistic.route("/content/")
def content():
    return render_template("dashboard/main.html")


@statistic.route("/schedule/")
def schedule():
    return render_template("dashboard/main.html")
