from mib.dao.manager import Manager
from mib.models.notification import Notification
from mib import db

from typing import List

class NotificationManager(Manager):
       
    @staticmethod
    def create_notification(notification : Notification):
        Manager.create(notification=notification)

    @staticmethod
    def retrieve_by_id(id_):
        notifications = db.session\
                        .query(Notification)\
                        .filter(Notification.is_notified == False, 
                                Notification.id == id_)\
                        .all()
        
        notify_list = []
        for notify in notifications:
            notify.is_notified = True
            notify_list.append(notify)
        db.session.commit()

        sender_notify = list(filter(lambda n: n.for_sender == True, notify_list))
        recipient_notify = list(filter(lambda n: n.for_recipient == True, notify_list))
        lottery_notify = list(filter(lambda n: n.for_lottery == True, notify_list))

        map_dictionary = lambda n: {
            "id_user": n.id_user,
            "id_message": n.id_message,
            "is_notified": n.is_notified,
            "from_recipient": n.from_recipient,
            "for_sender": n.for_sender,
            "for_recipient": n.for_recipient,
            "for_lottery": n.for_lottery,
        }

        sender_notify = list(map(map_dictionary, sender_notify))
        recipient_notify = list(map(map_dictionary, recipient_notify))
        lottery_notify = list(map(map_dictionary, lottery_notify))

        return {
            "sender_notify": sender_notify,
            "recipient_notify": recipient_notify,
            "lottery_notify": lottery_notify,
        }
        

    
        