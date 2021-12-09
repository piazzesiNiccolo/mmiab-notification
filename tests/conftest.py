import pytest
from mock.mock import patch
from mib import create_app
from mib.models.notification import Notification
from datetime import datetime
from mib import db


@pytest.fixture(scope="session", autouse=True)
def test_client():
    app = create_app()
    ctx = app.app_context()
    ctx.push()
    with app.test_client() as client:
        yield client


@pytest.fixture
def mock_rbi():
    with patch(
        "mib.dao.notification_manager.NotificationManager.retrieve_by_id"
    ) as mock:
        yield mock


@pytest.fixture
def mock_cn():
    with patch(
        "mib.dao.notification_manager.NotificationManager.create_notification"
    ) as mock:
        yield mock


"""@pytest.fixture
def notifications():
    notification1 = Notification(
        id_user = 1,
        id_message = 1,
        for_sender = True,
        for_recipient = False,
        for_lottery = False,
    )

    notification2 = Notification(
        id_user = 1,
        id_message = 2,
        for_sender = False,
        for_recipient = True,
        for_lottery = False,
        from_recipient = 2,
    )

    notification3 = Notification(
        id_user = 1,
        for_sender = False,
        for_recipient = False,
        for_lottery = True
    )

    db.session.add(notification1)
    db.session.add(notification2)
    db.session.add(notification3)
    db.session.commit()
    yield notification1, notification2, notification3
    db.session.delete(notification1)
    db.session.delete(notification2)
    db.session.delete(notification3)
    db.session.commit()"""
