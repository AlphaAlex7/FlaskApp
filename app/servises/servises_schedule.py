import datetime
from sqlalchemy import or_, and_
from ..models import ScheduleRegular, ScheduleContent, db


def content_to_pub(*, hours=1, minutes=0):
    irregular_query = get_irregular_query(hours=hours, minutes=minutes)
    irregular = irregular_query.all()
    regular = get_schedule_regular(
        subquery=irregular_query.subquery(),
        hours=hours,
        minutes=minutes
    )
    return regular, irregular


def get_schedule_regular(*, subquery=None, hours: int = 1, minutes: int = 0):
    time_from, time_to = time_interval(hours=hours, minutes=minutes)
    if subquery is not None:
        schedule_regular = db.session.query(
            ScheduleRegular, subquery.c.id
        ).outerjoin(
            subquery,
            and_(
                subquery.c.channel_id == ScheduleRegular.channel_id,
                subquery.c.time_pub == ScheduleRegular.time_pub,
            ),
            isouter=True)
    else:
        schedule_regular = db.session.query(
            ScheduleRegular
        )

    if time_from > time_to:
        schedule_regular = schedule_regular \
            .filter(
            or_(
                ScheduleRegular.time_pub > time_from,
                ScheduleRegular.time_pub < time_to
            ))
    else:
        schedule_regular = schedule_regular \
            .filter(ScheduleRegular.time_pub.between(time_from, time_to))

    if subquery is not None:
        return [
            regular
            for regular, irregular in schedule_regular.all()
            if irregular is None
        ]
    else:
        return schedule_regular.all()


def get_irregular(*, query=None, hours: int = 1):
    if query:
        return query.all()
    else:
        return get_irregular_query(hours=hours).all()


def get_irregular_query(hours: int = 1, minutes: int = 0):
    date_from, date_to = date_interval(hours=hours, minutes=minutes)
    if date_from.time() > date_to.time():
        irregular = db.session.query(ScheduleContent) \
            .filter(
            or_(
                and_(
                    ScheduleContent.time_pub > date_from.time(),
                    ScheduleContent.date_pub == date_from.date()
                ),
                and_(
                    ScheduleContent.time_pub < date_to.time(),
                    ScheduleContent.date_pub == date_to.date()
                )
            ))
    else:
        irregular = db.session.query(ScheduleContent) \
            .filter(
            and_(
                ScheduleContent.date_pub.between(
                    date_from.date(), date_to.date()
                ),
                ScheduleContent.time_pub.between(
                    date_from.time(), date_to.time()
                )))

    return irregular


def time_interval(*args, **kwargs):
    return get_time_next(), get_time_next(*args, **kwargs)


def date_interval(*args, **kwargs):
    return get_datetime_now(), get_datetime_now(*args, **kwargs)


def get_datetime_increment(*args, **kwargs):
    hours = kwargs.get("hours", 0)
    minutes = kwargs.get("minutes", 0)
    result_time = datetime.datetime.today() \
                  + datetime.timedelta(hours=hours, minutes=minutes)
    return result_time


def get_time_next(*args, **kwargs):
    now = get_datetime_increment(*args, **kwargs)
    return datetime.time(hour=now.hour, minute=now.minute)


def get_datetime_now(*args, **kwargs):
    now = get_datetime_increment(*args, **kwargs)
    date_now = datetime.date(year=now.year, month=now.month, day=now.day)
    time_now = datetime.time(hour=now.hour, minute=now.minute)
    return datetime.datetime.combine(date_now, time_now)
