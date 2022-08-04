import datetime

from sqlalchemy.sql.expression import func

from .models import db, User, Role, \
    Channel, ChannelStatistic, ChannelContent, \
    ScheduleContent, ScheduleRegular
from .servises.enum_helpers import ScheduleRegularType
import string
import random


def create_test_data():
    create_role()
    generator_list = [
        user_generator,
        test_channel_generator,
        test_channel_content_generator,
        channel_state_generator,
        test_schedule_content_generator,
        test_schedule_regular_generator
    ]
    for i in generator_list:
        create_items(i())


def create_role():
    Role.insert_roles()


def create_items(generator):
    db.session.add_all(generator)
    db.session.commit()


def user_generator():
    user_name = ["ieshua", "aga", "miga"]
    role = Role.query.filter_by(name="User").first()
    for i in user_name:
        yield User(username=i,
                   password="123456",
                   email=f"{i}@a.ru",
                   role=role)


def channel_generator():
    users = User.query.all()
    for i in range(10):
        yield Channel(
            slug_name="".join([
                random.choice(string.ascii_letters)
                for _ in range(5)
            ]),
            channel_id="".join([
                random.choice(string.ascii_letters)
                for _ in range(20)
            ]),
            name="".join([
                random.choice(string.ascii_letters)
                for _ in range(20)
            ]),
            author=random.choice(users)
        )


def channel_content_generator():
    channels = Channel.query.all()
    for channel in channels:
        for i in range(50):
            random_pub = (i % random.randrange(3, 7)) == 0
            slug = "".join([
                random.choice(string.ascii_letters)
                for _ in range(10)
            ])
            date_created = datetime.datetime.now() \
                           - datetime.timedelta(days=random.randrange(1, 40),
                                                hours=random.randrange(1, 20))
            if random_pub:
                date_pub = datetime.datetime.now() \
                           - datetime.timedelta(days=random.randrange(1, 20),
                                                hours=random.randrange(1, 20))

            yield ChannelContent(
                title=slug,
                text_content="".join([
                    random.choice(string.ascii_letters)
                    for _ in range(10)
                ]),
                date_created=date_created,
                date_pub=date_pub if random_pub else None,
                number_of_views=random.randrange(100,
                                                 5000) if random_pub else None,
                pub=True if random_pub else False,
                channel_id=channel.id
            )


def channel_state_generator():
    for i in Channel.query.all():
        stat = 0
        rand_int = random.randrange(1, 10)
        days_delta = random.randrange(1, 10) + 50
        while True:
            stat += random.randint(-5, 50)

            yield ChannelStatistic(
                followers=stat,
                channel=i,
                date=(datetime.datetime.now()
                      - datetime.timedelta(days=days_delta))
            )
            days_delta -= 1

            if days_delta == 0:
                break

        stat += random.randint(1, 50)
        yield ChannelStatistic(
            followers=stat,
            channel=i,
            date=(datetime.datetime.now()
                  - datetime.timedelta(days=days_delta))
        )


def schedule_content_generator():
    for channel in Channel.query.all():
        content = ChannelContent.query.filter_by(
            channel_id=channel.id
        ).order_by(
            func.random()
        ).limit(13).all()

        for i in content:
            date = datetime.datetime.now() \
                   + datetime.timedelta(days=random.randrange(2, 10),
                                        hours=random.randrange(0, 20))
            yield ScheduleContent(
                channel_id=i.channel_id,
                content_id=i.id,
                datetime_pub=date,
            )


def schedule_regular_generator():
    for i in Channel.query.all():
        for _ in range(5):
            time = datetime.time(hour=random.randrange(0, 23), minute=10)
            yield ScheduleRegular(
                channel_id=i.id,
                time_pub=time,
                content_type=random.choice(list(ScheduleRegularType))
            )


def test_channel_generator():
    user = User.query.filter_by(username="ieshua").first()
    for i in range(2):
        yield Channel(
            slug_name=f"test_{i}",
            channel_id=f"test_id_{i}",
            name=f"test_{user.username}_channel_{i}",
            author=user
        )


def test_channel_content_generator():
    channels = Channel.query.all()
    for channel in channels:
        for i in range(50):
            date_created = datetime.datetime.now() \
                           - datetime.timedelta(days=i)
            if i < 20:
                date_pub = datetime.datetime.now() \
                           - datetime.timedelta(hours=i)
                number_of_views = i * 10
                pub = True
            else:
                date_pub = None
                number_of_views = None
                pub = False

            yield ChannelContent(
                title=f"content_{channel}_{i}",
                text_content=f"text_content_{channel}_{i}",
                date_created=date_created,
                date_pub=date_pub,
                number_of_views=number_of_views,
                pub=pub,
                channel_id=channel.id
            )


def test_schedule_content_generator():
    for channel in Channel.query.all():
        content = ChannelContent.query.filter_by(
            channel_id=channel.id, pub=False
        ).limit(20).all()
        date_start = datetime.datetime.combine(
            datetime.datetime.now().date(),
            datetime.time(hour=0, minute=10)
        )
        for index, item in enumerate(content):
            if index == 2 and channel.id==2:
                continue
            date = date_start + datetime.timedelta(hours=index * 2)
            yield ScheduleContent(
                channel_id=item.channel_id,
                content_id=item.id,
                datetime_pub=date,
            )


def test_schedule_regular_generator():
    for i in Channel.query.all():
        for j in range(12):
            time = datetime.time(hour=j * 2, minute=10)
            yield ScheduleRegular(
                channel_id=i.id,
                time_pub=time,
                content_type=list(ScheduleRegularType)[j % 3]
            )
