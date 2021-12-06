import json
import logging

from mib import db
from mib.dao.notification_manager import NotificationManager
from mib.models.notification import Notification
def add_notify(message):
    if message["type"] == "message":
        payload = json.loads(message["data"])
        notifications = payload.get("notifications")
        notifications =[Notification(
            id_message=n["id_message"],
            id_user=n["id_user"],
            for_recipient=n["for_recipient"],
            for_sender=n["for_sender"],
            for_lottery=n["for_lottery"],
            from_recipient=n["from_recipient"]
        ) for n in notifications]
        db.session.add_all(notifications)
        NotificationManager.update()
        logging.info(f"removed participant with user_id {id}")
