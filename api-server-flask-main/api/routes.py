# -*- encoding: utf-8 -*-


from datetime import datetime, timezone, timedelta

from functools import wraps

from flask import request
from flask_restx import Api, Resource, fields

import jwt

from .models import db, Users, JWTTokenBlocklist
from .config import BaseConfig
import requests

import moodle_api
from moodle_api import Attendance 
#from sys_models import SurveySystem

#system = SurveySystem()




rest_api = Api(version="1.0", title="Users API")


"""
    Flask-Restx models for api request and response data
"""

signup_model = rest_api.model('SignUpModel', {"username": fields.String(required=True, min_length=2, max_length=32),
                                              "email": fields.String(required=True, min_length=4, max_length=64),
                                              "password": fields.String(required=True, min_length=4, max_length=16)
                                              })

login_model = rest_api.model('LoginModel', {"email": fields.String(required=True, min_length=4, max_length=64),
                                            "password": fields.String(required=True, min_length=4, max_length=16)
                                            })

user_edit_model = rest_api.model('UserEditModel', {"userID": fields.String(required=True, min_length=1, max_length=32),
                                                   "username": fields.String(required=True, min_length=2, max_length=32),
                                                   "email": fields.String(required=True, min_length=4, max_length=64)
                                                   })



"""
   Helper function for JWT token required
"""

def token_required(f):

    @wraps(f)
    def decorator(*args, **kwargs):

        token = None

        if "authorization" in request.headers:
            token = request.headers["authorization"]

        if not token:
            return {"success": False, "msg": "Valid JWT token is missing"}, 400

        try:
            data = jwt.decode(token, BaseConfig.SECRET_KEY, algorithms=["HS256"])
            current_user = Users.get_by_email(data["email"])

            if not current_user:
                return {"success": False,
                        "msg": "Sorry. Wrong auth token. This user does not exist."}, 400

            token_expired = db.session.query(JWTTokenBlocklist.id).filter_by(jwt_token=token).scalar()

            if token_expired is not None:
                return {"success": False, "msg": "Token revoked."}, 400

            if not current_user.check_jwt_auth_active():
                return {"success": False, "msg": "Token expired."}, 400

        except:
            return {"success": False, "msg": "Token is invalid"}, 400

        return f(current_user, *args, **kwargs)

    return decorator


"""
    Flask-Restx routes
"""


@rest_api.route('/api/users/register')
class Register(Resource):
    """
       Creates a new user by taking 'signup_model' input
    """

    @rest_api.expect(signup_model, validate=True)
    def post(self):

        req_data = request.get_json()

        _username = req_data.get("username")
        _email = req_data.get("email")
        _password = req_data.get("password")

        user_exists = Users.get_by_email(_email)
        if user_exists:
            return {"success": False,
                    "msg": "Email already taken"}, 400

        new_user = Users(username=_username, email=_email)

        new_user.set_password(_password)
        new_user.save()

        return {"success": True,
                "userID": new_user.id,
                "msg": "The user was successfully registered"}, 200


@rest_api.route('/api/users/login')
class Login(Resource):
    """
       Login user by taking 'login_model' input and return JWT token
    """

    @rest_api.expect(login_model, validate=True)
    def post(self):

        req_data = request.get_json()

        _email = req_data.get("email")
        _password = req_data.get("password")

        user_exists = Users.get_by_email(_email)

        if not user_exists:
            return {"success": False,
                    "msg": "This email does not exist."}, 400

        if not user_exists.check_password(_password):
            return {"success": False,
                    "msg": "Wrong credentials."}, 400

        # create access token uwing JWT
        token = jwt.encode({'email': _email, 'exp': datetime.utcnow() + timedelta(minutes=30)}, BaseConfig.SECRET_KEY)

        user_exists.set_jwt_auth_active(True)
        user_exists.save()

        return {"success": True,
                "token": token,
                "user": user_exists.toJSON()}, 200


@rest_api.route('/api/users/edit')
class EditUser(Resource):
    """
       Edits User's username or password or both using 'user_edit_model' input
    """

    @rest_api.expect(user_edit_model)
    @token_required
    def post(self, current_user):

        req_data = request.get_json()

        _new_username = req_data.get("username")
        _new_email = req_data.get("email")

        if _new_username:
            self.update_username(_new_username)

        if _new_email:
            self.update_email(_new_email)

        self.save()

        return {"success": True}, 200


@rest_api.route('/api/users/logout')
class LogoutUser(Resource):
    """
       Logs out User using 'logout_model' input
    """

    @token_required
    def post(self, current_user):

        _jwt_token = request.headers["authorization"]

        jwt_block = JWTTokenBlocklist(jwt_token=_jwt_token, created_at=datetime.now(timezone.utc))
        jwt_block.save()

        self.set_jwt_auth_active(False)
        self.save()

        return {"success": True}, 200


@rest_api.route('/api/sessions/oauth/github/')
class GitHubLogin(Resource):
    def get(self):
        code = request.args.get('code')
        client_id = BaseConfig.GITHUB_CLIENT_ID
        client_secret = BaseConfig.GITHUB_CLIENT_SECRET
        root_url = 'https://github.com/login/oauth/access_token'

        params = { 'client_id': client_id, 'client_secret': client_secret, 'code': code }

        data = requests.post(root_url, params=params, headers={
            'Content-Type': 'application/x-www-form-urlencoded',
        })

        response = data._content.decode('utf-8')
        access_token = response.split('&')[0].split('=')[1]

        user_data = requests.get('https://api.github.com/user', headers={
            "Authorization": "Bearer " + access_token
        }).json()
        
        user_exists = Users.get_by_username(user_data['login'])
        if user_exists:
            user = user_exists
        else:
            try:
                user = Users(username=user_data['login'], email=user_data['email'])
                user.save()
            except:
                user = Users(username=user_data['login'])
                user.save()
        
        user_json = user.toJSON()

        token = jwt.encode({"username": user_json['username'], 'exp': datetime.utcnow() + timedelta(minutes=30)}, BaseConfig.SECRET_KEY)
        user.set_jwt_auth_active(True)
        user.save()

        return {"success": True,
                "user": {
                    "_id": user_json['_id'],
                    "email": user_json['email'],
                    "username": user_json['username'],
                    "token": token,
                }}, 200
    

    #main page route
@rest_api.route('/')
def index():
    return 'Hello User. Welcome to the Moodle Attendance API'

#attendance route for all data
#first API route, all columns
@rest_api.route('/all')
def get_all():
    out=moodle_api.call("gradereport_user_get_grade_items",courseid=2)
    correct_json=out["usergrades"]
    lst_dict=[]
    for i in range(len(correct_json)):
        lst_dict.append({'userid':correct_json[i]['userid'],'username':correct_json[i]['userfullname'],
                   'courseid':correct_json[i]['courseid'], 'examscore':correct_json[i]['gradeitems'][1]['gradeformatted'],
                    'quiztotal':correct_json[i]['gradeitems'][2]['gradeformatted'],
                     'journal':correct_json[i]['gradeitems'][3]['gradeformatted'],
                    'attendance':correct_json[i]['gradeitems'][4]['gradeformatted'],
                    'attendance_plugin':correct_json[i]['gradeitems'][5]['graderaw']})

    return {'all':lst_dict}

#second api route - just attendance
@rest_api.route('/attendance')
def get_attendance():
    out=moodle_api.call("gradereport_user_get_grade_items",courseid=2)
    correct_json=out["usergrades"]
    lst_dict=[]
    for i in range(len(correct_json)):
        lst_dict.append({'userid':correct_json[i]['userid'],'username':correct_json[i]['userfullname'],
                    'attendance':correct_json[i]['gradeitems'][5]['gradeformatted']})

    return {'attendance':lst_dict}

#third Route to Get attendance values by userid
@rest_api.route('/attendance/<userid>')
def get_attendan(userid):
    valueattendance=Attendance.query.get(userid)
    if valueattendance is None:
        return {"error":"Userid not found try again"}
    else:
        return {"username":valueattendance.username,"userid":valueattendance.userid,"attendance score":valueattendance.attendance}

    
    #questions route - displays question pool
# @rest_api.route("/questions")
# def questions():

#      if not system.check_login() == 3: return redirect(url_for('index'))

#      mandatory_questions = Question.query.filter_by(state = 1, required = 1).all()
#      optional_questions = Question.query.filter_by(state = 1, required = 0).all()

#      if request.args.get('delete'):
#          if request.args.get('delete') == '1':
#              return render_template("questions.html", mandatory_questions=mandatory_questions, optional_questions=optional_questions, success=1)
#          else:
#              return render_template("questions.html", mandatory_questions=mandatory_questions, optional_questions=optional_questions, error=1)
#      else:
#          return render_template("questions.html", mandatory_questions=mandatory_questions, optional_questions=optional_questions)