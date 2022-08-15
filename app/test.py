import unittest
import freezegun

import datetime
from flask import url_for
from app import create_app, db
from app.init_db_data import create_test_data
from app.servises.servises_schedule import get_irregular, \
    get_schedule_regular, time_interval, date_interval, content_to_pub


class FlaskClientTestCase(unittest.TestCase):
    schedule_time = [
        "00:00:00",
        "04:30:00",
        "23:30:00"
    ]

    def setUp(self):
        self.app = create_app('test')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        create_test_data()
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_get_schedule_content(self):
        for t in self.schedule_time:
            with self.subTest():
                with freezegun.freeze_time(
                        f"{datetime.date.today().isoformat()} {t}"
                ):
                    print(datetime.date.today())
                    print(date_interval())
                    print()
                    print(get_schedule_regular(hour=2))
                    print()
                    print(get_irregular(hour=2))
                    print()
                    print(content_to_pub(2))
                    print()

        # for rule in self.app.url_map.iter_rules():
        #     with self.subTest(f"rule {rule.endpoint}"):
        #         response = self.client.get(url_for(rule.endpoint, _external=True))
        #         print(response.status_code)
        #         self.assertTrue(200 == response.status_code)
