import json
import pytest
from mib import db
from mib.dao.notification_manager import NotificationManager
from mib.events.callbacks import remove_notify_user_delete, add_notify
from mib.models.notification import Notification


class TestCallbacks:
    @pytest.mark.parametrize("type", ["foo", "message"])
    def test_add_notify(self, type):
        payload = {
            "type": type,
            "data": json.dumps(
                {
                    "notifications": [
                        {
                            "id_message": 1,
                            "id_user": 1,
                            "for_recipient": True,
                            "for_sender": False,
                            "for_lottery": False,
                            "from_recipient": None,
                        },
                        {
                            "id_message": 4,
                            "id_user": 3,
                            "for_recipient": False,
                            "for_sender": True,
                            "for_lottery": False,
                            "from_recipient": 2,
                        },
                    ]
                }
            ),
        }
        add_notify(payload)
        if type == "foo":
            assert db.session.query(Notification).all() == []
        else:
            assert len(db.session.query(Notification).all()) == 2
            db.session.query(Notification).delete()
            db.session.commit()

    @pytest.mark.parametrize("type", ["foo", "message"])
    def test_delete_notify(self, type):
        db.session.query(Notification).delete()
        notification1 = Notification(
            id_user=1,
            id_message=1,
            for_sender=True,
            for_recipient=False,
            for_lottery=False,
        )

        notification2 = Notification(
            id_user=1,
            id_message=2,
            for_sender=False,
            for_recipient=True,
            for_lottery=False,
            from_recipient=2,
        )

        notification3 = Notification(
            id_user=1, for_sender=False, for_recipient=False, for_lottery=True
        )

        db.session.add(notification1)
        db.session.add(notification2)
        db.session.add(notification3)
        db.session.commit()
        assert db.session.query(Notification).all() == [
            notification1,
            notification2,
            notification3,
        ]
        payload = {"type": type, "data": json.dumps({"user_id": 1})}
        remove_notify_user_delete(payload)
        if type == "foo":
            assert db.session.query(Notification).all() == [
                notification1,
                notification2,
                notification3,
            ]
            db.session.delete(notification1)
            db.session.delete(notification2)
            db.session.delete(notification3)
            db.session.commit()
        else:
            assert db.session.query(Notification).all() == []
