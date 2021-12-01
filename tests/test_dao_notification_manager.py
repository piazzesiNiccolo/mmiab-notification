from mib import db
from mib.models.notification import Notification
from mib.dao.notification_manager import NotificationManager


class TestNotificationManager:

    def test_create_notification_manager(self):
        notify = Notification(
            id_user = 1, 
            id_message = 1, 
            for_sender = True
            )

        NotificationManager.create_notification(notify)

        assert db.session.query(Notification).count() == 1

        db.session.delete(notify)
        db.session.commit()

    def test_get_notification(self):

        notify_sender = Notification(
            id_user = 1, 
            id_message = 1, 
            for_sender = True,
            from_recipient = 2,
            is_notified = False
            )
        notify_recipient = Notification(
            id_user = 1, 
            id_message = 2, 
            for_recipient = True,
            is_notified = False
            )
        notify_lottery = Notification(
            id_user = 1, 
            for_lottery = True,
            is_notified = False
            )
        
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
