from app import db

class User(db.Model):
    # id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False,primary_key=True)
    password = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(120), nullable=True)
    NotifyToken = db.Column(db.String(120), nullable=True)
    Line_uuid = db.Column(db.String(120), nullable=True)
    mqtt_dongle_id = db.Column(db.String(120), nullable=True)
    phone_number = db.Column(db.String(120), nullable=True)

    children = db.relationship('Notify_status',back_populates="parent",cascade="all, delete-orphan")
    def __repr__(self):
        return '{username=%s,email=%s,NotifyToken=%s}' % (
            self.username,
            self.email,
            self.NotifyToken
            )

class Notify_status(db.Model):
    username = db.Column(db.String(100), db.ForeignKey('user.username'), nullable=True, primary_key=True)
    Device_Mac= db.Column(db.String(100), primary_key=True)
    Device_status=db.Column(db.Boolean(), nullable=True)
    Device_type= db.Column(db.String(100),nullable=True)

    parent = db.relationship('User',back_populates="children")

    def __repr__(self):
        return '{username=%s,Device_Mac=%s,Device_status=%s,Device_type=%s}' % (
            self.username,
            self.Device_Mac,
            self.Device_status,
            self.Device_type
            )

