from flask import render_template, request, redirect, url_for
from flask_login import current_user
from . import statistic


@statistic.route("/")
def start():
    return redirect(url_for("statistic.subscribe"))


@statistic.route("/subscribe/")
def subscribe():
    return render_template("dashboard/statistic_subscribe.html", path_url="subscribe")


@statistic.route("/content/")
def content():
    return render_template("dashboard/main.html")


@statistic.route("/schedule/")
def schedule():
    return render_template("dashboard/main.html")
