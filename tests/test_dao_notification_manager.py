from mib import db
from mib.models.notification import Notification
from mib.dao.notification_manager import NotificationManager
from testing.fake_response import MockResponse
import mock
import pytest
import requests


class TestNotificationManager:
    def test_create_notification_manager(self):
        notify = Notification(id_user=1, id_message=1, for_sender=True)

        NotificationManager.create_notification(notify)

        assert db.session.query(Notification).count() == 1

        db.session.delete(notify)
        db.session.commit()

    def test_get_notification(self):

        notify_sender = Notification(
            id_user=1,
            id_message=1,
            for_sender=True,
            from_recipient=2,
            is_notified=False,
        )
        notify_recipient = Notification(
            id_user=1, id_message=2, for_recipient=True, is_notified=False
        )
        notify_lottery = Notification(id_user=1, for_lottery=True, is_notified=False)

        db.session.add(notify_sender)
        db.session.add(notify_recipient)
        db.session.add(notify_lottery)
        db.session.commit()

        notification = NotificationManager.retrieve_by_id(1)
        assert notification["sender_notify"][0]["for_sender"] == True
        assert notification["recipient_notify"][0]["for_recipient"] == True
        assert notification["lottery_notify"][0]["for_lottery"] == True

        db.session.delete(notify_sender)
        db.session.delete(notify_recipient)
        db.session.delete(notify_lottery)
        db.session.commit()

    def test_retrieve_users_info_no_ids(self):
        assert NotificationManager.retrieve_users_info([]) == {}

    @pytest.mark.parametrize("code,length", [(200, 2), (404, 0)])
    def test_retrieve_users_info_ok(
        self, code, length
    ):  ##id femail first name last name  phone nickname lottery_points
        with mock.patch("requests.get") as m:
            m.return_value = MockResponse(
                code=code,
                json={
                    "users": [
                        {
                            "id": 1,
                            "email": "email@email.com",
                            "firstname": "name",
                            "lastname": "name",
                            "phone": 123456789,
                            "nickname": "nick",
                            "lottery_points": 1,
                        },
                        {
                            "id": 2,
                            "email": "email1@email1.com",
                            "firstname": "name1",
                            "lastname": "name1",
                            "phone": 134256789,
                            "nickname": "nick1",
                            "lottery_points": 2,
                        },
                    ]
                },
            )
            d = NotificationManager.retrieve_users_info([1, 2])
            assert len(d) == length

    @pytest.mark.parametrize("ex", [requests.ConnectionError, requests.ConnectTimeout])
    def test_retrieve_user_info_bad_response(self, ex):
        with mock.patch("requests.get") as m:
            m.side_effect = ex()
            d = NotificationManager.retrieve_users_info([1, 2])
            assert d == {}
            m.reset_mock(side_effect=True)

    def test_retrieve_by_id(self):
        notify_sender = Notification(
            id_user=1,
            id_message=1,
            for_sender=True,
            from_recipient=2,
            is_notified=False,
        )
        notify_sender2 = Notification(
            id_user=1,
            id_message=3,
            for_sender=True,
            from_recipient=None,
            is_notified=False,
        )
        notify_recipient = Notification(
            id_user=1, id_message=2, for_recipient=True, is_notified=False
        )
        notify_lottery = Notification(id_user=1, for_lottery=True, is_notified=False)

        db.session.add(notify_sender)
        db.session.add(notify_sender2)
        db.session.add(notify_recipient)
        db.session.add(notify_lottery)
        db.session.commit()
        with mock.patch(
            "mib.dao.notification_manager.NotificationManager.retrieve_users_info"
        ) as m:
            m.return_value = {
                1: {
                    "email": "email@email.com",
                    "firstname": "name",
                    "lastname": "name",
                    "phone": 123456789,
                    "nickname": "nick",
                    "lottery_points": 1,
                },
                2: {
                    "email": "email1@email1.com",
                    "firstname": "name1",
                    "lastname": "name1",
                    "phone": 134256789,
                    "nickname": "nick1",
                    "lottery_points": 2,
                },
            }
            d = NotificationManager.retrieve_by_id(1)
            assert len(d["sender_notify"]) == 2
            assert len(d["recipient_notify"]) == 1
            assert len(d["lottery_notify"]) == 1
            db.session.query(Notification).delete()
