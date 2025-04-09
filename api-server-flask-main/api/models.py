# -*- encoding: utf-8 -*-


from datetime import datetime

import json

from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

import ast
db = SQLAlchemy()

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(64), nullable=True)
    password = db.Column(db.Text())
    jwt_auth_active = db.Column(db.Boolean())
    date_joined = db.Column(db.DateTime(), default=datetime.utcnow)
    courses = db.relationship('Course', backref='users', lazy=True)

    def __repr__(self):
        return f"Users {self.username}"

    def save(self):
        db.session.add(self)
        db.session.commit()

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def update_email(self, new_email):
        self.email = new_email

    def update_username(self, new_username):
        self.username = new_username

    def check_jwt_auth_active(self):
        return self.jwt_auth_active

    def set_jwt_auth_active(self, set_status):
        self.jwt_auth_active = set_status

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)

    @classmethod
    def get_by_email(cls, email):
        return cls.query.filter_by(email=email).first()
    
    @classmethod
    def get_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    def toDICT(self):

        cls_dict = {}
        cls_dict['_id'] = self.id
        cls_dict['username'] = self.username
        cls_dict['email'] = self.email

        return cls_dict

    def toJSON(self):

        return self.toDICT()


class JWTTokenBlocklist(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    jwt_token = db.Column(db.String(), nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False)

    def __repr__(self):
        return f"Expired Token: {self.jwt_token}"

    def save(self):
        db.session.add(self)
        db.session.commit()

#Тестирование

class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    questions = db.relationship('Question', backref='test', lazy=True)
    def __repr__(self):
        return f'<Test {self.title}>'

class Question(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer, primary_key=True)
    test_id = db.Column(db.Integer, db.ForeignKey('test.id'), nullable=False)
    question_text = db.Column(db.String(250), nullable=False)
    options = db.relationship('Option', backref='question', lazy=True)
    def __repr__(self):
        return f'<Question {self.question_text}>'

class Option(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    option_text = db.Column(db.String(100), nullable=False)
    is_correct = db.Column(db.Boolean, default=False)
    def __repr__(self):
        return f'<Option {self.option_text}>'

class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    test_id = db.Column(db.Integer, db.ForeignKey('test.id'), nullable=False)
    score = db.Column(db.Float, nullable=False)
    def __repr__(self):
        return f'<Result User ID: {self.user_id}, Test ID: {self.test_id}, Score: {self.score}>'

class Course(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

