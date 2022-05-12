from flask import render_template, request, redirect, url_for
from flask_login import current_user

from . import statistic
from ..servises import get_channels_for_user, get_date_for_filter, \
    get_color_for_graf, get_channels_for_menu, \
    get_content_for_chanel, get_content_table_head, \
    get_content_table_body, get_option_sort_content


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
    sorting = request.args.get("sorting", "title_asc")
    page = int(request.args.get("page", 1))

    channels = get_channels_for_user(current_user)
    table_head = get_content_table_head()

    content_pagination = get_content_for_chanel(
        current_user=current_user,
        id=id,
        page=page,
        sorting=sorting
    )

    table_row = get_content_table_body(content_pagination.items)
    option_sort = get_option_sort_content(id=id)

    return render_template(
        "dashboard/content_page.html",
        channels=get_channels_for_menu(channels),
        id=id,
        table_head=table_head,
        table_row=table_row,
        pagination=content_pagination,
        sorting="&sorting="+sorting,
        option_sort=option_sort
    )


@statistic.route("/schedule/<int:id>")
def schedule(id):
    channels = get_channels_for_user(current_user)
    return render_template(
        "dashboard/main.html",
        channels=get_channels_for_menu(channels)
    )
