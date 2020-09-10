from c_and_c import db


company_briefing_table = db.Table('company_briefing_table',
    db.Column('briefing_id', db.Integer, db.ForeignKey('briefing.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
)


class UserCompanyTable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=False)
    company_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=False)
    access_count = db.Column(db.Integer)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    type = db.Column(db.Integer, nullable=False)
    topic = db.Column(db.String(1000), nullable=True, unique=False)
    history = db.relationship('History', backref='user', lazy=True)


class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(1000), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=False)


class Briefing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(1000), nullable=False)
    participants = db.relationship('User', backref='briefings', secondary=company_briefing_table, lazy=True)


class Lecture(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(1000), nullable=False)


def init():
    db.create_all()
