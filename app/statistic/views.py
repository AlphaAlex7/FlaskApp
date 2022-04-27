from flask import render_template, request
from flask_login import current_user
from . import statistic


@statistic.route("/")
def start():
    if current_user:
        print(current_user)
    return render_template("main.html")

