from flask import render_template, request, redirect, url_for
from flask_login import current_user
from . import statistic
from ..servises import get_channels_for_user, get_date_for_filter, get_color_for_graf, get_channels_for_menu, \
    get_content_for_chanel, get_table_context


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
        option_date=option_date,
        channels=get_channels_for_menu(channels),
    )


@statistic.route("/content/<int:id>/")
def content(id):
    channels = get_channels_for_user(current_user)
    print(get_channels_for_menu(channels))
    return render_template(
        "dashboard/content_page.html",
        channels=get_channels_for_menu(channels),
        id = id
    )


@statistic.route("/content_table/<int:id>/")
def content_table(id):
    content = get_content_for_chanel(current_user=current_user, id=id, page=int(request.args.get("page")))
    table_head, table_row = get_table_context(content)

    return render_template(
        "dashboard/table_template.html",
        table_head=table_head,
        table_row=table_row
    )


@statistic.route("/schedule/<int:id>")
def schedule(id):
    channels = get_channels_for_user(current_user)
    return render_template(
        "dashboard/main.html",
        channels=get_channels_for_menu(channels)
    )
