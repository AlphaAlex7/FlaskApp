from datetime import datetime

from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user

from . import statistic
from .. import db
from ..servises.servises import get_channels_for_user, get_date_for_filter, \
    get_color_for_graf, get_channels_for_menu, \
    get_content_for_chanel, get_option_sort_content, get_regular_schedule, get_content_schedule, rename_channel, \
    create_channel
from ..servises.form_helper import do_disable_forms, form_to_model, model_to_form
from ..servises.table_helper import get_content_table_head, get_regular_schedule_table_head, \
    get_content_schedule_table_head, get_channel_table_head, get_content_table_body, get_regular_schedule_table_body, \
    get_content_schedule_table_body, get_channel_table_body
from ..servises.enum_helpers import ScheduleRegularType, FlashType
from .forms import ContentDetailForm, RegularScheduleForm, \
    ContentScheduleAddForm, ContentScheduleDeleteForm, \
    NewChannelForm, RenameChannelForm, SearchContentForm
from ..models import ChannelContent, ScheduleRegular, ScheduleContent


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
    table_head = get_channel_table_head()
    table_row = get_channel_table_body(channels)
    return render_template(
        "dashboard/channel/statistic_subscribe.html",
        option_channel=option_channel,
        option_date=option_date,
        channels=get_channels_for_menu(channels),
        table_head=table_head,
        table_row=table_row,
    )


@statistic.route("/channel_detail/", methods=["GET", "POST"])
def channel_detail():
    id_channel = int(request.args.get("id_channel", 0))
    if id_channel:
        form = RenameChannelForm()
    else:
        form = NewChannelForm()
    channels = get_channels_for_user(current_user)

    if request.method == "GET":
        if id_channel:
            try:
                current_channel = list(filter(lambda x: x.id == id_channel, channels))[0]
                model_to_form(form, current_channel)
            except IndexError:
                return render_template('404.html', error_message="А конкретно этого канала"), 404
        return render_template(
            "dashboard/channel/channel_detail.html",
            channels=get_channels_for_menu(channels),
            form=form
        )
    elif request.method == "POST":
        if form.validate_on_submit():
            if id_channel:
                rename_channel(id_channel, form)
            else:
                create_channel(current_user, form)
            return redirect(url_for("statistic.subscribe"))
        return render_template(
            "dashboard/channel/channel_detail.html",
            channels=get_channels_for_menu(channels),
            form=form
        )


@statistic.route("/content/<int:id>/")
def content(id):
    sorting = request.args.get("sorting", "title_asc")
    page = int(request.args.get("page", 1))
    search = request.args.get("search")

    channels = get_channels_for_user(current_user)
    table_head = get_content_table_head()
    form_search = SearchContentForm()

    if form_search.validate_on_submit():
        search = form_search.search.data

    if search:
        form_search.search.data = search

    content_pagination = get_content_for_chanel(
        current_user=current_user,
        id=id,
        page=page,
        sorting=sorting,
        search=search
    )

    table_row = get_content_table_body(content_pagination.items)
    option_sort = get_option_sort_content(id=id)

    return render_template(
        "dashboard/content/content_page.html",
        channels=get_channels_for_menu(channels),
        id=id,
        table_head=table_head,
        table_row=table_row,
        pagination=content_pagination,
        sorting="&sorting=" + sorting,
        option_sort=option_sort,
        form_search=form_search,
        searching=f"&search={search}" if search else ""
    )


@statistic.route("/content_detail/", methods=["GET", "POST"])
def content_detail():
    form = ContentDetailForm()
    channels = get_channels_for_user(current_user)
    form.channel_id.choices = [(i.id, i.name) for i in channels]
    id_post = int(request.args.get("id_post", 0))
    id_channel = int(request.args.get("id_channel", 0))
    post = None
    form_schedule = None
    action_schedule_form = None

    if request.method == "GET":
        if id_post:
            post = ChannelContent.query.get(id_post)
            model_to_form(form, post)
            if post.pub:
                do_disable_forms(form)
            if post.schedule:
                form_schedule = ContentScheduleDeleteForm()
                form_schedule.datetime_pub.data = post.schedule.datetime_pub
                form_schedule.id_schedule.data = post.schedule.id

                action_schedule_form = url_for("statistic.schedule_delete") + f'?id_post={id_post}'

                if request.referrer:
                    if url_for("statistic.content_schedule", id=id_channel) in request.referrer:
                        action_schedule_form += f"&referer_schedule={True}"
                        action_schedule_form += f"&id_channel={id_channel}"
            else:
                form_schedule = ContentScheduleAddForm()
                action_schedule_form = url_for("statistic.schedule_add") + f'?id_post={id_post}'


        elif id_channel:
            form.channel_id.data = id_channel
        return render_template(
            "dashboard/content/content_detail.html",
            form=form,
            channels=get_channels_for_menu(channels),
            post=post,
            form_schedule=form_schedule,
            action_schedule_form=action_schedule_form
        )

    else:
        if form.validate_on_submit():
            if id_post:
                post = ChannelContent.query.get(id_post)
            else:
                post = ChannelContent()

            form_to_model(form, post)
            db.session.add(post)
            db.session.commit()
            return redirect(f'{url_for("statistic.content_detail")}?id_post={post.id}')


@statistic.route("/content_detail/schedule_add", methods=["POST"])
def schedule_add():
    id_post = int(request.args.get("id_post", 0))
    form = ContentScheduleAddForm()
    if form.validate_on_submit():
        if datetime.now() < form.datetime_pub.data:
            content = ChannelContent.query.get(id_post)
            new_schedule = ScheduleContent(
                content_id=content.id,
                channel_id=content.channel_id,
                datetime_pub=form.datetime_pub.data
            )
            db.session.add(new_schedule)
            db.session.commit()
    return redirect(f'{url_for("statistic.content_detail")}?id_post={id_post}')


@statistic.route("/content_detail/schedule_delete", methods=["POST"])
def schedule_delete():
    id_post = int(request.args.get("id_post", 0))
    referer = request.args.get("referer_schedule")
    id_channel = request.args.get("id_channel")
    form = ContentScheduleDeleteForm()
    if form.validate_on_submit():
        db.session.delete(ScheduleContent.query.get(form.id_schedule.data))
        db.session.commit()
        if referer:
            return redirect(
                url_for("statistic.content_schedule", id=id_channel))

    return redirect(f'{url_for("statistic.content_detail")}?id_post={id_post}')


@statistic.route("/schedule/<int:id>", methods=["GET", "POST"])
def schedule(id):
    page = int(request.args.get("page", 1))
    channels = get_channels_for_user(current_user)

    try:
        current_channel = next(filter(lambda x: x.id == id, channels))
    except StopIteration:
        current_channel = None

    regular_schedule_pagination = get_regular_schedule(current_channel, page=page)
    table_head = get_regular_schedule_table_head()
    table_row = get_regular_schedule_table_body(regular_schedule_pagination.items)

    return render_template(
        "dashboard/schedule/regular_schedule.html",
        channels=get_channels_for_menu(channels),
        id=id,
        table_head=table_head,
        table_row=table_row,
        pagination=regular_schedule_pagination
    )


@statistic.route("/schedule_regular_form/<int:id_channel>/", methods=["GET", "POST"])
def schedule_regular_form(id_channel):
    id_schedule = int(request.args.get("id_schedule_regular", 0))
    form_regular_schedule = RegularScheduleForm()
    form_regular_schedule.content_type.choices = [(i.name, i.name) for i in ScheduleRegularType]

    if request.method == "GET":
        action = url_for("statistic.schedule_regular_form", id_channel=id_channel)
        if id_schedule:
            regular_schedule = ScheduleRegular.query.get(id_schedule)

            model_to_form(form_regular_schedule, regular_schedule)

            action += f"?id_schedule_regular={id_schedule}"
        else:
            form_regular_schedule.delete.render_kw = {"hidden": ""}
        return render_template(
            "dashboard/api_templates/form.html",
            form=form_regular_schedule,
            action=action)
    else:
        if form_regular_schedule.validate_on_submit():
            if id_schedule:
                regular_schedule = ScheduleRegular.query.get(id_schedule)
                if form_regular_schedule.delete.data:
                    db.session.delete(regular_schedule)
                    db.session.commit()
                    return redirect(
                        url_for("statistic.schedule", id=id_channel))
            else:
                regular_schedule = ScheduleRegular()

            form_to_model(form_regular_schedule, regular_schedule)
            regular_schedule.channel_id = id_channel

            db.session.add(regular_schedule)
            db.session.commit()

        return redirect(
            url_for("statistic.schedule", id=id_channel))


@statistic.route("/content_schedule/<int:id>", methods=["GET", "POST"])
def content_schedule(id):
    page = int(request.args.get("page", 1))
    channels = get_channels_for_user(current_user)

    try:
        current_channel = next(filter(lambda x: x.id == id, channels))
    except StopIteration:
        current_channel = None

    content_schedule_pagination = get_content_schedule(current_channel, page=page)

    table_head = get_content_schedule_table_head()
    table_row = get_content_schedule_table_body(content_schedule_pagination.items)

    return render_template(
        "dashboard/schedule/content_schedule.html",
        channels=get_channels_for_menu(channels),
        id=id,
        table_head=table_head,
        table_row=table_row,
        pagination=content_schedule_pagination
    )
