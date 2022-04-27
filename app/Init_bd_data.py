import datetime

from .models import db, User, Role, Channel, ChannelStatistic
import string
import random


def create_role():
    Role.insert_roles()


def create_user():
    user_name = ["ieshua", "aga", "miga"]
    role = Role.query.filter_by(name="User").first()
    for i in user_name:
        us = User(username=i,
                  password="123456",
                  email=f"{i}@a.ru",
                  role=role)
        db.session.add(us)
    db.session.commit()


def create_channel():
    users = User.query.all()
    for i in range(10):
        ch = Channel(
            slug_name="".join([random.choice(string.ascii_letters) for i in range(5)]),
            channel_id="".join([random.choice(string.ascii_letters) for i in range(20)]),
            name="".join([random.choice(string.ascii_letters) for i in range(20)]),
            author=random.choice(users)
        )
        db.session.add(ch)
        db.session.commit()


def create_channel_stat():
    channel = Channel.query.all()
    for i in channel:
        print(f"stat for {i.slug_name}")
        stat = 0
        rand_int = random.randrange(1, 10)
        for j in range(50, 0, -1):
            stat += random.randint(1, 50)
            statistic = ChannelStatistic(
                followers=stat,
                channel=i,
                date=(datetime.datetime.now() - datetime.timedelta(days=j + rand_int))
            )
            db.session.add(statistic)
            db.session.commit()


if __name__ == '__main__':
    create_role()
    create_user()
