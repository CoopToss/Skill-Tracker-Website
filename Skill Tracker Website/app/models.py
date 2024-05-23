from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(256), index=True, unique=True)
    email = db.Column(db.String(256), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    goals = db.relationship('Goal', backref='user', overlaps="goals, user", lazy='dynamic')
    skills = db.relationship('Skill', backref='user', lazy=True)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Goal(db.Model):
    __tablename__ = 'goal'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    associated_user = db.relationship('User', backref='associated_goals')

class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140))
    hours_logged = db.Column(db.Integer, default=0)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.id'))  
    goal = db.relationship('Goal', backref='skills')  
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    goal_details = db.Column(db.Text, nullable=True)

class SkillLog(db.Model):
    __tablename__ = 'skill_logs'

    id = db.Column(db.Integer, primary_key=True)
    hours = db.Column(db.Integer)
    date = db.Column(db.DateTime)
    skill_id = db.Column(db.Integer, db.ForeignKey('skills.id'))