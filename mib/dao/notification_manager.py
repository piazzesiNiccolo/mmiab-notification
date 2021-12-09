import requests
from mib.models.notification import Notification
from mib import db
from flask import current_app as app


class NotificationManager():
    """
    Wrapper class  for all db operations involving notification
    """
       
    @classmethod
    def users_endpoint(cls):
        return app.config['USERS_MS_URL']
    
    @classmethod
    def requests_timeout_seconds(cls):
        return app.config['REQUESTS_TIMEOUT_SECONDS']

    @classmethod
    def create_notification(cls, notification : Notification):
        db.session.add(notification)
        db.session.commit()

    @classmethod
    def retrieve_users_info(cls, ids):
        if len(ids) == 0:
            return {}

        ids_str = ','.join([str(id) for id in ids])
        endpoint = f"{cls.users_endpoint()}/users/display_info?ids={ids_str}"
        try:
            response = requests.get(endpoint, timeout=cls.requests_timeout_seconds())
            if response.status_code == 200:
                recipients = response.json()['users']
                formatted_rcp = {}
                for rcp in recipients:
                    _id = rcp['id']
                    del rcp['id']
                    formatted_rcp[_id] = rcp
                return formatted_rcp
            else:
                return {}

        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            return {}

    @classmethod
    def retrieve_by_id(cls, id_):
        notifications = db.session\
                        .query(Notification)\
                        .filter(Notification.is_notified == False, 
                                Notification.id_user == id_)\
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

        rcp_for_sender = [n['from_recipient'] for n in sender_notify]
        rcp_for_sender = list(set(rcp_for_sender))
        user_dict = cls.retrieve_users_info(rcp_for_sender)
        for n in sender_notify:
            user = user_dict.get(n['from_recipient'], None)
            if user is not None:
                _fn, _ln = user.get('first_name', 'Anonymous'), user.get('last_name', '')
                n['from_recipient'] = (_fn + ' ' + _ln).strip()
            else:
                n['from_recipient'] = 'Anonymous'

        return {
            "sender_notify": sender_notify,
            "recipient_notify": recipient_notify,
            "lottery_notify": lottery_notify,
        }
        
