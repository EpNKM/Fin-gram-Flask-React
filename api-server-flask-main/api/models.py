# -*- encoding: utf-8 -*-


from datetime import datetime

import json

from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

import ast
db = SQLAlchemy()

class Users(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(64), nullable=True)
    password = db.Column(db.Text())
    jwt_auth_active = db.Column(db.Boolean())
    date_joined = db.Column(db.DateTime(), default=datetime.utcnow)

    def __repr__(self):
        return f"User {self.username}"

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

class User(db.Model):

    __tablename__ = 'USERS'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    type = db.Column(db.Integer, nullable=False)

class Course(db.Model):

    __tablename__ = 'COURSES'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(10), nullable=False)
    session = db.Column(db.String(5), nullable=False)

class Enrolment(db.Model):

    __tablename__ = 'ENROLMENTS'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    u_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    c_id = db.Column(db.Integer, db.ForeignKey(Course.id), nullable=False)
    user = db.relationship(User)
    course = db.relationship(Course)

class Question(db.Model):

    __tablename__ = 'QUESTIONS'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    text = db.Column(db.Text, nullable=False)
    state = db.Column(db.Integer, nullable=False)
    type = db.Column(db.Integer, nullable=False)
    required = db.Column(db.Integer, nullable=False)
    responses = db.Column(db.Text, nullable=False)

    def responsesList(self):
         return ast.literal_eval(self.responses)

class Survey(db.Model):

    __tablename__ = 'SURVEYS'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.Text, nullable=False)
    c_id = db.Column(db.Integer, db.ForeignKey(Course.id), nullable=False)
    state = db.Column(db.Integer, nullable=False)
    questions = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now())
    course = db.relationship(Course)

    def questionsList(self):
         return ast.literal_eval(self.questions)

class Response(db.Model):

    __tablename__ = 'RESPONSES'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    u_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    s_id = db.Column(db.Integer, db.ForeignKey(Survey.id), nullable=False)
    q_id = db.Column(db.Integer, db.ForeignKey(Question.id), nullable=False)
    text = db.Column(db.Text)
    num = db.Column(db.Integer)
    user = db.relationship(User)
    survey = db.relationship(Survey)
    question = db.relationship(Question)

    def responsesList(self):
         return ast.literal_eval(self.responses)
    
class Attendance(db.Model):
    userid=db.Column(db.Integer,primary_key=True)
    courseid=db.Column(db.Integer)
    examscore=db.Column(db.String(120))
    quiztotal=db.Column(db.String(120))
    journal=db.Column(db.String(120))
    attendance=db.Column(db.String(120))
    attendance_plugin=db.Column(db.String(120))
    username=db.Column(db.String(80),unique=True,nullable=False)
    

    def __repr__(self):
        return f"{self.userid}-{self.username}-{self.examscore}-{self.quiztotal}-{self.journal}-{self.attendance_plugin}"
    
#Adding all selected contents into a table built with SQLALCHEMY
# out=moodle_api.call("gradereport_user_get_grade_items",courseid=2)
# correct_json=out["usergrades"]
# lst_dict=[]
# db.create_all()
# for i in range(len(correct_json)):
#         lst_dict.append({'userid':correct_json[i]['userid'],'username':correct_json[i]['userfullname'],
#                    'courseid':correct_json[i]['courseid'], 'examscore':correct_json[i]['gradeitems'][1]['gradeformatted'],
#                     'quiztotal':correct_json[i]['gradeitems'][2]['gradeformatted'],
#                      'journal':correct_json[i]['gradeitems'][3]['gradeformatted'],
#                     'attendance':correct_json[i]['gradeitems'][4]['gradeformatted'],
#                     'attendance_plugin':correct_json[i]['gradeitems'][5]['graderaw']})
# for i in range(len(lst_dict)):
#         value1=Attendance(username=lst_dict[i]['username'], userid=lst_dict[i]['userid'],examscore=lst_dict[i]['examscore'],quiztotal=lst_dict[i]['quiztotal'], journal=lst_dict[i]['journal'], attendance=lst_dict[i]['attendance'])
#         db.session.add(value1)
#         db.session.commit()
