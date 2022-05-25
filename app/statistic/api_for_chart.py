from flask import request
from flask_login import current_user

from ..servises.servises import get_channels_for_user, add_main_statistic_to_answer, \
    add_average_subscribers_statistic_to_answer, add_average_content_views_statistic_to_answer
from . import statistic
from ..servises.dict_helper import get_update_dict


@statistic.route("/api_chart/channel-main-chart/", methods=["GET"])
def statistic_channel_for_current_user():
    channels = get_channels_for_user(current_user, id=request.args.get("channel_id"))
    answer = get_update_dict()
    for channel in channels:
        add_main_statistic_to_answer(answer, channel, days_delta=int(request.args.get("days_delta", 20)))
    return answer


@statistic.route("/api_chart/channel-average-subscribers/", methods=["GET"])
def average_subscribers_channel_for_current_user():
    channels = get_channels_for_user(current_user, id=request.args.get("channel_id"))
    answer = get_update_dict()
    for channel in channels:
        add_average_subscribers_statistic_to_answer(answer, channel)
    answer["columns"].sort(key=lambda x: x[1])
    return answer


@statistic.route("/api_chart/channel-average-content-views/", methods=["GET"])
def average_content_views_channel_for_current_user():
    channels = get_channels_for_user(current_user, id=request.args.get("channel_id"))
    answer = get_update_dict()
    for channel in channels:
        add_average_content_views_statistic_to_answer(answer, channel)
    answer["columns"].sort(key=lambda x: x[1])
    return answer
