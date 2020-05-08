from flask import request, jsonify
from flask_restplus import Namespace, Resource, fields
from marshmallow import Schema, fields as ma_fields, post_load
from flaskblog import db, bcrypt
from flaskblog.models import User
from flaskblog.users.utils import send_reset_email

api = Namespace('users', description='Users endpoints')

create_user_model = api.model('Model', {
    'username': fields.String(),
    'email': fields.String(),
    'password': fields.String(),
})


class TheUser(object):
    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return 'User {} has been created'.format(self.username)


class UserSchema(Schema):
    id = ma_fields.Integer()
    username = ma_fields.String(required=True)
    password = ma_fields.String(required=True)
    email = ma_fields.Email(required=True)

    @post_load
    def create_user(self, data):
        return TheUser(**data)


user_schema = UserSchema()
users_schema = UserSchema(many=True)


@api.route('/')
class UserActions(Resource):
    @api.expect(create_user_model)
    def post(self):
        data = request.get_json()
        username = data['username']
        email = data['email']
        hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')

        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return user_schema.dump(new_user), 201


@api.route('/<int:user_id>')
class UserGetter(Resource):
    def get(self, user_id):
        users = User.query.get(user_id)
        return user_schema.dump(users)

    @api.expect(create_user_model)
    def put(self, user_id):
        data = request.get_json()
        username = data['username']
        email = data['email']
        user = User.query.get(user_id)
        user.username = username
        user.email = email
        db.session.commit()

        return user_schema.dump(user)

    def delete(self, user_id):
        user = User.query.get(user_id)
        db.session.delete(user)
        db.session.commit()
        return user_schema.dump(user)


@api.route('/all')
class UsersGetter(Resource):
    def get(self):
        users = User.query.all()
        return users_schema.dump(users)


@api.route('/reset-password')
class UsersResetPassword(Resource):
    def post(self):
        data = request.get_json()
        email = data['email']
        user = User.query.filter_by(email=email).first()
        send_reset_email(user)
        return jsonify({'message': 'email has been sent'})
