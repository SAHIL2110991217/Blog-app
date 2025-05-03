from flask import Blueprint
from flask_restful import Api
from App.api.wrapper.apis import LoginResource, LogoutResource, HomePageResource,RegisterResource, CommentResource,PostResource
from App.api.logger import log_route_access

route = Blueprint('route', __name__)
api_v1 = Api(route)

api_v1.add_resource(RegisterResource, '/register')
log_route_access('RegisterResource', '/register')

api_v1.add_resource(LoginResource, '/login')
log_route_access('LoginResource', '/login')

api_v1.add_resource(LogoutResource, '/logout')
log_route_access('LogoutResource', '/logout')

api_v1.add_resource(HomePageResource, '/home')
log_route_access('HomePageResource', '/home')

api_v1.add_resource(PostResource, '/post', '/post/<uuid:post_id>')
log_route_access('PostResource', '/post')

api_v1.add_resource(CommentResource, '/posts/<uuid:post_id>/comments', '/comments/<uuid:comment_id>')
log_route_access('CommentResource', '/posts/<uuid:post_id>/comments')