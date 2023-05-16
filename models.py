from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    __table_args__ = {'schema': 'public'}

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    birth_year = db.Column(db.Integer, nullable=False)
    country = db.Column(db.String(3), nullable=False)
    currency = db.Column(db.String(3), nullable=False)
    gender = db.Column(db.String(6), nullable=False)
    registration_date = db.Column(db.DateTime, nullable=False)

    def __init__(self, user_json):
        self.birth_year = user_json.get('birth_year')
        self.country = user_json.get('country')
        self.currency = user_json.get('currency')
        self.gender = user_json.get('gender')
        self.registration_date = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

    def to_json(self):
        return {
            'user_id': self.user_id,
            'birth_year': self.birth_year,
            'country': self.country,
            'currency': self.currency,
            'gender': self.gender,
            'registration_date': self.registration_date
        }


class Coupon(db.Model):
    __tablename__ = 'coupons'
    __table_args__ = {'schema': 'public'}

    coupon_id = db.Column(db.String, primary_key=True)
    stake = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.user_id))

    def __init__(self, coupon_json):
        self.coupon_id = coupon_json.get('coupon_id')
        self.stake = coupon_json.get('stake')
        self.timestamp = datetime.strptime(coupon_json.get('timestamp'), '%Y-%m-%d %H:%M:%S')
        self.user_id = coupon_json.get('user_id')

    def to_json(self):
        return {
            'coupon_id': self.coupon_id,
            'stake': self.stake,
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'user_id': self.user_id
        }


class Event(db.Model):
    __tablename__ = 'events'
    __table_args__ = {'schema': 'public'}

    event_id = db.Column(db.String, primary_key=True)
    begin_timestamp = db.Column(db.DateTime, nullable=False)
    end_timestamp = db.Column(db.DateTime, nullable=False)
    country = db.Column(db.String, nullable=False)
    league = db.Column(db.String, nullable=False)
    participants = db.Column(db.ARRAY(db.String), nullable=False)
    sport = db.Column(db.String, nullable=False)

    def __init__(self, event_json):
        self.event_id = event_json.get('event_id')
        self.begin_timestamp = datetime.strptime(event_json.get('begin_timestamp'), '%Y-%m-%d %H:%M:%S')
        self.end_timestamp = datetime.strptime(event_json.get('end_timestamp'), '%Y-%m-%d %H:%M:%S')
        self.country = event_json.get('country')
        self.league = event_json.get('league')
        self.participants = event_json.get('participants')
        self.sport = event_json.get('sport')

    def to_json(self):
        return {
            'event_id': self.event_id,
            'begin_timestamp': self.begin_timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'end_timestamp': self.end_timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'country': self.country,
            'league': self.league,
            'participants': self.participants,
            'sport': self.sport
        }


class Selection(db.Model):
    __tablename__ = 'selections'
    __table_args__ = {'schema': 'public'}

    event_id = db.Column(db.String, db.ForeignKey(Event.event_id), primary_key=True)
    coupon_id = db.Column(db.String, db.ForeignKey(Coupon.coupon_id), primary_key=True)
    odds = db.Column(db.Float, nullable=False)

    def __init__(self, selection_json):
        self.event_id = selection_json.get('event_id')
        self.coupon_id = selection_json.get('coupon_id')
        self.odds = selection_json.get('odds')

    def to_json(self):
        return {
            'event_id': self.event_id,
            'coupon_id': self.coupon_id,
            'odds': self.odds
        }
