import json
import logging

from mib import db
from mib.models.notification import Notification


def add_notify(message):
    if message["type"] == "message":
        payload = json.loads(message["data"])
        notifications = payload.get("notifications")
        notifications = [
            Notification(
                id_message=n["id_message"],
                id_user=n["id_user"],
                for_recipient=n["for_recipient"],
                for_sender=n["for_sender"],
                for_lottery=n["for_lottery"],
                from_recipient=n["from_recipient"],
            )
            for n in notifications
        ]
        db.session.add_all(notifications)
        db.session.commit()


def remove_notify_user_delete(message):
    if message["type"] == "message":
        payload = json.loads(message["data"])
        id = payload.get("user_id")
        db.session.query(Notification).filter(Notification.id_user == id).delete()
        db.session.commit()
        logging.info(f"removed notifications for user with id {id}")
