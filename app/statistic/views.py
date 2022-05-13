from flask import render_template, request, redirect, url_for
from flask_login import current_user

from . import statistic
from .. import db
from ..servises import get_channels_for_user, get_date_for_filter, \
    get_color_for_graf, get_channels_for_menu, \
    get_content_for_chanel, get_content_table_head, \
    get_content_table_body, get_option_sort_content, do_disable_forms
from .forms import ContentDetailForm
from ..models import ChannelContent


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
        sorting="&sorting=" + sorting,
        option_sort=option_sort
    )


@statistic.route("/content_detail/", methods=["GET", "POST"])
def content_detail():
    form = ContentDetailForm()
    channels = get_channels_for_user(current_user)
    form.channel_id.choices = [(i.id, i.name) for i in channels]
    id_post = int(request.args.get("id_post", 0))
    id_channel = int(request.args.get("id_channel", 0))
    post = None

    if form.validate_on_submit():
        if id_post:
            post = ChannelContent.query.get(id_post)
        else:
            post = ChannelContent()
        post.title = form.title.data
        post.text_content = form.text_content.data
        post.channel_id = form.channel_id.data
        db.session.add(post)
        db.session.commit()
        return redirect(
            url_for("statistic.content", id=form.channel_id.data))

    if id_post:
        post = ChannelContent.query.get(id_post)
        form.channel_id.data = post.channel_id
        form.title.data = post.title
        form.text_content.data = post.text_content
        if post.pub:
            do_disable_forms(form)
    elif id_channel:
        form.channel_id.data = id_channel

    return render_template(
        "dashboard/content_detail.html",
        form=form,
        channels=get_channels_for_menu(channels),
        post=post
    )


@statistic.route("/schedule/<int:id>")
def schedule(id):
    channels = get_channels_for_user(current_user)
    return render_template(
        "dashboard/main.html",
        channels=get_channels_for_menu(channels)
    )
