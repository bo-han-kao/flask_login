from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(120), nullable=True)
    NotifyToken = db.Column(db.String(120), nullable=True)
    Line_uuid = db.Column(db.String(120), nullable=True)
    ip = db.Column(db.String(120), nullable=True)
    G1_mac = db.Column(db.String(120), nullable=True)
    senser=db.Column(db.Boolean(),default=True)
    SW=db.Column(db.Boolean(),default=True)
    G1=db.Column(db.Boolean(),default=True)
    def __repr__(self):
        return '{username=%s,email=%s,NotifyToken=%s}' % (
            self.username,
            self.email,
            self.NotifyToken
            )

class pre_status(db.Model):
    id = db.Column(db.String(20), primary_key=True)
    on_off = db.Column(db.String(10), nullable=False)
    ip = db.Column(db.String(30), nullable=False)
    def __repr__(self):
        return '{id=%s,email=%s,on_off=%s,ip=%s}' % (
            self.id,
            self.on_off,
            self.ip
            )