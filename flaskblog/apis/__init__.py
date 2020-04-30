from flask_restplus import Api

from .users import api as users_namespace
from .posts import api as posts_namespace

api = Api(
    title='Learning app',
    version='1.0',
    description='A description',
)

api.add_namespace(users_namespace, path='/api/users')
api.add_namespace(posts_namespace, path='/api/posts')
