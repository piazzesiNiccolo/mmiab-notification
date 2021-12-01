from flask import request, jsonify

from mib.dao.notification_manager import NotificationManager
from mib.models.notification import Notification

def notifications(id):

    notifications = NotificationManager.retrieve_by_id(id)

    response = jsonify(
        {
            "status" : "success",
            "message" : "Notifications have been sent correctly",
            "data" : notifications,
        }
    )
    return response, 200

def add_notifications():

    data = request.get_json()

    notifications = data.get("data")

    for n in notifications:
        notification = Notification(
            id_user = n["id_user"],
            id_message = n["id_message"],
            for_sender = n["for_sender"],
            for_recipient = n["for_recipient"],
            for_lottery = n["for_lottery"],
            from_recipient = n["from_recipient"]
        )
        NotificationManager.create_notification(notification)

    response = jsonify(
        {
            "status" : "success",
            "message" : "Notifications added correctly"
        }
    )

    return response, 200
