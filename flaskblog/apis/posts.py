from flask import request
from flask_restplus import Namespace, Resource, fields
from marshmallow import Schema, fields as ma_fields, post_load
from flaskblog import db
from flaskblog.models import Post
from flaskblog.utils.token_required import token_required

api = Namespace('posts', description='Posts endpoints')
create_post_model = api.model('Model', {
    'title': fields.String(),
    'content': fields.String(),
    'user_id': fields.Integer(),
})


class ThePost(object):
    def __init__(self, title, content, user_id):
        self.title = title
        self.content = content
        self.user_id = user_id

    def __repr__(self):
        return 'User {} has been created'.format(self.title)


class PostSchema(Schema):
    id = ma_fields.Integer()
    title = ma_fields.String(required=True)
    content = ma_fields.String(required=True)
    user_id = ma_fields.Integer(required=True)
    date_posted = ma_fields.DateTime(required=True)

    @post_load
    def create_post(self, data):
        return ThePost(**data)


user_schema = PostSchema()
users_schema = PostSchema(many=True)


@api.route('/')
class UserActions(Resource):
    @api.expect(create_post_model)
    def post(self):
        data = request.get_json()
        title = data['title']
        content = data['content']
        user_id = data['user_id']

        new_post = Post(title=title, content=content, user_id=user_id)
        db.session.add(new_post)
        db.session.commit()

        return user_schema.dump(new_post), 201


@api.route('/<int:post_id>')
class PostGetter(Resource):
    def get(self, post_id):
        post = Post.query.get(post_id)
        return user_schema.dump(post)

    @api.expect(create_post_model)
    def put(self, post_id):
        data = request.get_json()
        title = data['title']
        date_posted = data['date_posted']
        content = data['content']
        user_id = data['user_id']
        post = Post.query.get(post_id)
        post.title = title
        post.date_posted = date_posted
        post.date_posted = content
        post.date_posted = user_id
        db.session.commit()

        return user_schema.dump(post)

    def delete(self, post_id):
        post = Post.query.get(post_id)
        db.session.delete(post)
        db.session.commit()
        return user_schema.dump(post)


@api.route('/all')
class UsersGetter(Resource):
    @token_required
    def get(self):
        posts = Post.query.all()
        return users_schema.dump(posts)
