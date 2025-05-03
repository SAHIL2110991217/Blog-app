from flask import request
from flask_restful import Resource
from App.api.wrapper.utils import user_register, user_login, user_logout, get_comments, create_comment, update_comment, delete_comment
from flask_jwt_extended import jwt_required, get_jwt_identity
from App.api.logger import  error_logger
from App.api.wrapper.utils import (
    create_new_post, 
    get_post, 
    update_post, 
    delete_post, 
    get_home_page_data
)

class SomeProtectedResource(Resource):
    @jwt_required()
    def get(self):
        try:
            return {'message': 'This is a protected endpoint.'}, 200
        except Exception as e:
            error_logger('SomeProtectedResource', 'Failed to access protected endpoint', error=str(e))
            return {'message': 'Internal Server Error'}, 500
class RegisterResource(Resource):
    def post(self):
        try:
            data = request.get_json()
            response_data, status_code = user_register(data)
            return response_data, status_code
        except Exception as e:
            error_logger('RegisterResource', 'Registration failed', error=str(e))
            return {
                'message': 'Registration failed',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40003'}
            }, 400

class LoginResource(Resource):
    def post(self):
        try:
            data = request.get_json()
            response_data, status_code = user_login(data)
            return response_data, status_code
        except Exception as e:
            error_logger('LoginResource', 'Login failed', error=str(e))
            return {
                'message': 'Login failed',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40003'}
            }, 400

class LogoutResource(Resource):
    @jwt_required()
    def post(self):
        try:
            response_data, status_code = user_logout()
            return response_data, status_code
        except Exception as e:
            error_logger('LogoutResource', 'Logout failed', error=str(e))
            return {
                'message': 'Logout failed',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40003'}
            }, 400
        

class CommentResource(Resource):
    @jwt_required()
    def get(self, post_id):
        try:
            if post_id is None:
                return {
                'message': 'Post ID is required',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40006'}
            }, 400

            response_data, status_code = get_comments(post_id)
            return response_data, status_code
        except Exception as e:
            error_logger('CommentResource', 'Failed to get comments', post_id=post_id, error=str(e))
            return {
                'message': 'Failed to get comments',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40005'},
            }, 400
        
    @jwt_required()
    def post(self, post_id):
        try:
            if post_id is None:
                return {
                'message': 'Post ID is required',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40006'}
            }, 400

            user_id = get_jwt_identity()
            data = request.get_json()
            if not data or 'content' not in data:
                return {
                'message': 'Content is required',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40012'}
            }, 400
            response_data, status_code = create_comment(data, post_id, user_id)
            return response_data, status_code
        except Exception as e:
            error_logger('CommentResource', 'Failed to create comment', post_id=post_id, error=str(e))
            return {
                'message': 'Failed to create comment',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40005'}
            }, 400

    @jwt_required()
    def put(self, comment_id):
        try:
            if comment_id is None:
                return {
                    'message': 'Comment ID is required',
                    'status': False,
                    'type': 'custom_error',
                    'error_status': {'error_code': '40006'}
                    }, 400
            
            data = request.get_json()
            user_id = get_jwt_identity()
            if not data or 'content' not in data:
                return {
                'message': 'Content is required',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40012'}
            }, 400
            response_data, status_code = update_comment(data, comment_id, user_id)
            return response_data, status_code
        except Exception as e:
            error_logger('CommentResource', 'Failed to update comment', comment_id=comment_id, error=str(e))
            return {
                'message': 'Failed to update comment',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40005'},
            }, 400

    @jwt_required()
    def delete(self, comment_id):
        try:
            if comment_id is None:
                return {
                'message': 'Comment ID is required',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40006'}
                }, 400
            
            user_id = get_jwt_identity()
            response_data, status_code = delete_comment(comment_id, user_id)
            return response_data, status_code
        except Exception as e:
            error_logger('CommentResource', 'Failed to delete comment', comment_id=comment_id, error=str(e))
            return {
                'message': 'Failed to delete comment',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40005'},
            }, 400
        
class PostResource(Resource):
    @jwt_required()
    def post(self):
        try:
            data = request.get_json()
            response_data, status_code = create_new_post(data)
            return response_data, status_code
        except Exception as e:
            error_logger('PostResource', 'Error creating post', error=str(e))
            return {
                'message': 'Error creating post',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40000'}
            }, 400

    @jwt_required()
    def put(self, post_id):
        
        try:
            if post_id is None:
                return {
                    'message': 'Post ID is required',
                    'status': False,
                    'type': 'custom_error',
                    'error_status': {'error_code': '40006'}
                }, 400

            data = request.get_json()
            response_data, status_code = update_post(post_id, data)
            return response_data, status_code
        except Exception as e:
            error_logger('PostResource', 'Failed to update post', post_id=post_id, error=str(e))
            return {
                'message': 'Failed to update post',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40005'}
            }, 400


    @jwt_required()
    def get(self, post_id):
        try:
            if not post_id:
                return {
                    'message': 'Post ID is required',
                    'status': False,
                    'type': 'custom_error',
                    'error_status': {'error_code': '40006'}
                }, 400
            
            response_data, status_code = get_post(post_id)
            return response_data, status_code
        except Exception as e:
            error_logger('PostResource', 'Failed to get post', post_id=post_id, error=str(e))  
            return {
                'message': 'Failed to get post',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40005'}
            }, 400


    @jwt_required()
    def delete(self, post_id):
        try:
            if not post_id:
                return {
                    'message': 'Post ID is required',
                    'status': False,
                    'type': 'custom_error',
                    'error_status': {'error_code': '40006'}
                }, 400

            user_id = get_jwt_identity()
            response_data, status_code = delete_post(post_id, user_id)
            return response_data, status_code
        except Exception as e:
            error_logger('PostResource', 'Failed to delete post', post_id=post_id, error=str(e))
            return {
                'message': 'Failed to delete post',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40005'}
            }, 400

class HomePageResource(Resource):
    @jwt_required()
    def get(self):
        try:

            page = int(request.args.get('page', 1))
            size = int(request.args.get('size', 10))
            user_id = request.args.get('user', None)  

            if page < 1 or size < 1:
                raise ValueError("Page and size must be positive integers.")
            
            
            
            response_data, status_code = get_home_page_data(page, size, user_id)
            return response_data, status_code
        
        except ValueError as ve:
            error_logger('HomePageResource', 'Invalid pagination parameters', error=str(ve))
            return {
                'message': 'Invalid pagination parameters',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40016'}
            }, 400
        
        except Exception as e:
            error_logger('HomePageResource', 'Failed to retrieve home page data', error=str(e))
            return {
                'message': 'Failed to retrieve home page data',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40016'}
            }, 400