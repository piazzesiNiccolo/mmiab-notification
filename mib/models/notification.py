from mib import db

class Notification(db.Model):
    
    __tablename__ = "notification"

    id_notification = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_message = db.Column(db.Integer, default=None)
    id_user = db.Column(db.Integer)

    is_notified = db.Column(db.Boolean, default=False)
    for_recipient = db.Column(db.Boolean, default=False)
    for_sender = db.Column(db.Boolean, default=False)
    for_lottery = db.Column(db.Boolean, default=False)
    from_recipient = db.Column(db.Integer, default=None)

    # constructor of the notify object
    def __init__(self, *args, **kw):
        super(Notification, self).__init__(*args, **kw)