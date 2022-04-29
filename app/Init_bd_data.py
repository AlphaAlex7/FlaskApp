import datetime

from .models import db, User, Role, Channel, ChannelStatistic
import string
import random


def create_test_data():
    create_role()
    create_user()
    create_channel()
    create_channel_stat()


def create_role():
    Role.insert_roles()


def create_user():
    db.session.add_all(user_generator())
    db.session.commit()


def create_channel():
    db.session.add_all(channel_generator())
    db.session.commit()


def create_channel_stat():
    db.session.add_all(channel_state_generator())
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
            slug_name="".join([random.choice(string.ascii_letters) for i in range(5)]),
            channel_id="".join([random.choice(string.ascii_letters) for i in range(20)]),
            name="".join([random.choice(string.ascii_letters) for i in range(20)]),
            author=random.choice(users)
        )


def channel_state_generator():
    for i in Channel.query.all():
        stat = 0
        rand_int = random.randrange(1, 10)
        for j in range(50, 0, -1):
            stat += random.randint(1, 50)
            yield ChannelStatistic(
                followers=stat,
                channel=i,
                date=(datetime.datetime.now() - datetime.timedelta(days=j + rand_int))
            )
