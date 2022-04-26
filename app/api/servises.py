from ..models import ChannelStatistic


def add_statistic_to_answer(answer, channel):
    stat = ChannelStatistic.query.filter_by(channel=channel).all()
    answer[f"x_{channel.slug_name}"] = f"x_{channel.slug_name}"
    answer["xs"][channel.slug_name] = f"x_{channel.slug_name}"
    answer["columns"].append([channel.slug_name, *[i.followers for i in stat]])
    answer["columns"].append([f"x_{channel.slug_name}", *[i.date.strftime('%Y-%m-%d %H:%M:%S') for i in stat]])


def get_update_dict():
    return {"xs": {}, "columns": [], }
