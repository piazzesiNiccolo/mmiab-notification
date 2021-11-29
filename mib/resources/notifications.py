from flask import request, jsonify

from mib.dao.notification_manager import NotificationManager
from mib.dao.models import Notification

def notifications(user_id):

    notifications = NotificationManager.retrieve_by_id(user_id)

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

    for notification in notifications:
        NotificationManager.create_notification(Notification(notification))

    response = jsonify(
        {
            "status" : "success",
            "message" : "Notifications added correctly"
        }
    )
    

