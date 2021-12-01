import re
from mock.mock import patch, MagicMock, Mock
from mib import db
from tests.conftest import test_client
from mib.models.notification import Notification
from mib.dao.notification_manager import NotificationManager
import mock
import pytest

class TestNotificationServices:

    def test_notifications(self, test_client):
        #assert db.session.query(Notification).count() == 0

        obj = db.session.query(Notification).all()
        for ob in obj:
            db.session.delete(ob)
        db.session.commit()

        assert db.session.query(Notification).count() == 0
        data = {
            "data" : [{
            "id_user" : 1,
            "id_message" : 1,
            "for_sender" : True,
            "from_recipient" : 2,
            "for_recipient" : False,
            "for_lottery" : False
            },
            {
                "id_user" : 1,
                "id_message" : 2,
                "for_recipient" : True,
                "for_sender" : False,
                "for_lottery" : False,
                "from_recipient" : None
            },
            {
                "id_user" : 1,
                "for_lottery" : True,
                "id_message" : None,
                "for_recipient" : True,
                "for_sender" : False,
                "from_recipient" : None
            }
        ]}

        resp = test_client.post('/notifications/add', json=data)

        resp = test_client.get('/notifications/1')

        assert resp.status_code == 200
        assert resp.json["data"]["sender_notify"][0]["for_sender"] == True
        assert resp.json["data"]["recipient_notify"][0]["for_recipient"] == True
        assert resp.json["data"]["lottery_notify"][0]["for_lottery"] == True
        
    def test_add_notifications(self, test_client):

        data = {
            "data" : [{
            "id_user" : 1,
            "id_message" : 1,
            "for_sender" : True,
            "from_recipient" : 2,
            "for_recipient" : None,
            "for_lottery" : False
            },
            {
                "id_user" : 1,
                "id_message" : 2,
                "for_recipient" : True,
                "for_sender" : False,
                "for_lottery" : False,
                "from_recipient" : None
            },
            {
                "id_user" : 1,
                "for_lottery" : True,
                "for_sender" : False,
                "for_recipient" : False,
                "id_message" : None,
                "from_recipient" : None
            }
        ]}

        resp = test_client.post('/notifications/add', json=data)

        assert resp.status_code == 200
        assert resp.json["message"] == "Notifications added correctly"