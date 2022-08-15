import datetime
from sqlalchemy import or_, and_
from ..models import ScheduleRegular, ScheduleContent, db


def content_to_pub(hour):
    irregular_query = get_irregular_query(hour=hour)
    irregular = irregular_query.all()
    regular = get_schedule_regular(
        subquery=irregular_query.subquery(),
        hour=hour
    )
    return regular, irregular


def get_schedule_regular(*, subquery=None, hour: int = 1):
    time_from, time_to = time_interval(hour=hour)
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


def get_irregular(*, query=None, hour: int = 1):
    if query:
        return query.all()
    else:
        return get_irregular_query(hour=hour).all()


def get_irregular_query(hour: int = 1):
    date_from, date_to = date_interval(hour=hour)
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


def time_interval(*, hour: int = 1):
    return get_time_now(), get_time_now(increment_hour=hour)


def date_interval(*, hour: int = 1):
    return get_datetime_now(), get_datetime_now(increment_hour=hour)


def get_datetime_increment(increment_hour: int = 0):
    return datetime.datetime.today() + datetime.timedelta(
        hours=increment_hour)


def get_time_now(increment_hour: int = 0):
    now = get_datetime_increment(increment_hour=increment_hour)
    return datetime.time(hour=now.hour)


def get_datetime_now(increment_hour: int = 0):
    now = get_datetime_increment(increment_hour=increment_hour)
    date_now = datetime.date(year=now.year, month=now.month, day=now.day)
    time_now = datetime.time(hour=now.hour)
    return datetime.datetime.combine(date_now, time_now)
