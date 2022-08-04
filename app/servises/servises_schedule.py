import datetime
from sqlalchemy import or_, and_
from ..models import ScheduleRegular, ScheduleContent


def content_to_pub(hour):
    irregular = get_irregular(hour=hour)
    regular = get_schedule_regular(hour=hour)
    # TODO filter or correct get posts
    return regular, irregular


def get_schedule_regular(*,hour: int = 1):
    time_from, time_to = time_interval(hour=hour)
    if time_from > time_to:
        schedule_regular = ScheduleRegular.query \
            .filter(
            or_(
                ScheduleRegular.time_pub > time_from,
                ScheduleRegular.time_pub < time_to
            ))
    else:
        schedule_regular = ScheduleRegular.query \
            .filter(ScheduleRegular.time_pub.between(time_from, time_to))

    return schedule_regular.all()


def get_irregular(hour: int = 1):
    date_from, date_to = date_interval(hour=hour)
    irregular = ScheduleContent.query.filter(
        ScheduleContent.datetime_pub.between(
            date_from, date_to
        )
    ).all()
    return irregular


def time_interval(*, hour: int = 1):
    return get_time_now(), get_time_now(increment_hour=hour)


def date_interval(*, hour: int = 1):
    return get_datetime_now(), get_datetime_now(increment_hour=hour)


def get_datetime_increment(increment_hour: int = 0):
    return datetime.datetime.today() + datetime.timedelta(hours=increment_hour)


def get_time_now(increment_hour: int = 0):
    now = get_datetime_increment(increment_hour=increment_hour)
    return datetime.time(hour=now.hour)


def get_datetime_now(increment_hour: int = 0):
    now = get_datetime_increment(increment_hour=increment_hour)
    date_now = datetime.date(year=now.year, month=now.month, day=now.day)
    time_now = datetime.time(hour=now.hour)
    return datetime.datetime.combine(date_now, time_now)
