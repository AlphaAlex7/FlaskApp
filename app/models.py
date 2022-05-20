from datetime import datetime
from enum import Enum

from . import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin


class Permission:
    SEE = 1
    SEE_ALL = 2
    ADMIN = 16


class Role(db.Model):
    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    user = db.relationship("User", backref="role")
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)

    @staticmethod
    def insert_roles():
        roles = {
            'User': [Permission.SEE],
            'Moderator': [Permission.SEE, Permission.SEE_ALL],
            'Administrator': [Permission.SEE, Permission.SEE_ALL, Permission.ADMIN],
        }
        default_role = 'User'
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.reset_permissions()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default = (role.name == default_role)
            db.session.add(role)
        db.session.commit()

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm

    def reset_permissions(self):
        self.permissions = 0

    def has_permission(self, perm):
        return self.permissions & perm == perm

    def __repr__(self):
        return f"Role: {self.name}"


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"))
    password_hash = db.Column(db.String(128))
    channel = db.relationship("Channel", backref="author", lazy="joined")

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"User: {self.username}"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False

    def __eq__(self, other):
        return "AnonymousUser"

    def __repr__(self):
        return "AnonymousUser"

    def __str__(self):
        return "AnonymousUser"


login_manager.anonymous_user = AnonymousUser


class Channel(db.Model):
    __tablename__ = "channels"
    id = db.Column(db.Integer, primary_key=True)
    channel_id = db.Column(db.String(32), unique=True, index=True)
    name = db.Column(db.String(128))
    slug_name = db.Column(db.String(128), unique=True, index=True)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    statistics = db.relationship("ChannelStatistic", backref="channel", lazy="dynamic")
    content = db.relationship("ChannelContent", backref="channel", lazy="dynamic")
    schedule_regular = db.relationship("ScheduleRegular", backref="channel", lazy="dynamic")

    def __repr__(self):
        return f"Chanel: {self.slug_name}"


class ChannelStatistic(db.Model):
    __tablename__ = "channel_statistics"

    id = db.Column(db.Integer, primary_key=True)
    followers = db.Column(db.Integer)
    date = db.Column(db.DateTime(), default=datetime.utcnow)
    channel_id = db.Column(db.Integer, db.ForeignKey("channels.id"))

    def to_json(self):
        json_stat = {
            "followers": self.followers
        }
        return json_stat

    def __repr__(self):
        return f"Followers: {self.followers}"


class ChannelContent(db.Model):
    __tablename__ = "channel_content"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    text_content = db.Column(db.Text)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    date_pub = db.Column(db.DateTime, nullable=True)
    number_of_views = db.Column(db.Integer, nullable=True)
    pub = db.Column(db.Boolean, default=False)
    channel_id = db.Column(db.Integer, db.ForeignKey("channels.id"))
    schedule = db.relationship("ScheduleContent", backref="content", lazy="joined")

    def __repr__(self):
        return f"Content: {self.title}"


class ScheduleRegularType(Enum):
    NEW = 0
    OLD = 1
    RANDOM = 2


class ScheduleRegular(db.Model):
    __tablename__ = "schedule_regular"

    id = db.Column(db.Integer, primary_key=True)
    channel_id = db.Column(db.Integer, db.ForeignKey("channels.id"))
    content_type = db.Column(db.Enum(ScheduleRegularType), default=ScheduleRegularType.NEW)
    time_pub = db.Column(db.TIME)


class ScheduleContent(db.Model):
    __tablename__ = "schedule_content"

    id = db.Column(db.Integer, primary_key=True)
    channel_id = db.Column(db.Integer, db.ForeignKey("channels.id"))
    content_id = db.Column(db.Integer, db.ForeignKey("channel_content.id"))
    # content = db.relationship("ChannelContent", back_populates="schedule", lazy="joined")
    datetime_pub = db.Column(db.DateTime)
