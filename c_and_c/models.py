from c_and_c import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    type = db.Column(db.Integer, nullable=False)


def init():
    db.create_all()
