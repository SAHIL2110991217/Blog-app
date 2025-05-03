from sqlalchemy import desc
from App.Models.User.UserModel import User
from App.Models.Post.PostModel import Post
from App.Models.Comment.CommentModel import Comment
from App import db
from App.api.logger import error_logger  # Import logging functions


def get_user_by_username(username):
    try:
        user = User.query.filter_by(username=username).first()
        return user
    except Exception as e:
        error_logger('get_user_by_username', 'Failed to retrieve user', error=str(e), username=username)
        raise Exception("Database error")

def get_user_by_email(email):
    try:
        user = User.query.filter_by(email=email).first()
        return user
    except Exception as e:
        error_logger('get_user_by_email', 'Failed to retrieve user', error=str(e), email=email)
        raise Exception("Database error")

def get_user_by_user_id(uid):
    try:
        user=User.query.filter_by(uid=uid).first()
        return user
    except Exception as e:
        error_logger('get_user_by_uid', 'Failed to retrieve user', error=str(e), uid=uid)
        raise Exception("Database error")

def add_user(username, email, password):
    try:
        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        
        return new_user
    except Exception as e:
        db.session.rollback()
        error_logger('add_user', 'Failed to add user', error=str(e), username=username, email=email)
        raise Exception("Database error")

# Post Functions

def create_post(title, content, user_uid, username,image=None):
    try:
        new_post = Post(title=title, content=content, user_uid=user_uid, image=image, username=username)
        db.session.add(new_post)
        db.session.commit()
        
        return new_post
    except Exception as e:
        db.session.rollback()
        error_logger('create_post', 'Failed to create post', error=str(e), title=title, content=content)
        raise Exception("Database error")

def update_post(post_id, title, content, image=None):
    try:
        post = Post.query.filter_by(uid=post_id).first()
        if not post:
            error_logger('update_post', 'Post not found', post_id=post_id)
            return False

        if title:
            post.title = title
        if content:
            post.content = content
        if image is not None:
            post.image = image

        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        error_logger('update_post', 'Failed to update post', error=str(e), post_id=post_id)
        raise Exception("Database error")

def get_post_by_id(post_id):
    try:
        post = Post.query.filter_by(uid=post_id).first()
        if post:
            return post
        else:
            error_logger('get_post_by_id', 'Post not found', post_id=post_id)
            return None
    except Exception as e:
        error_logger('get_post_by_id', 'Failed to retrieve post', error=str(e), post_id=post_id)
        raise Exception("Database error")

def save_image(image_file, filename):
    try:
        image_path = f"App/api/uploads/{filename}"
        image_file.save(image_path)
        return filename
    except Exception as e:
        error_logger('save_image', 'Failed to save image', error=str(e), filename=filename)
        raise Exception("Database error")

def post_to_dict(post):
    return {
        'uid': str(post.uid),
        'title': post.title,
        'content': post.content,
        'user_uid': str(post.user_uid),
        'username':post.username,
        'created_at': post.created_at.isoformat(),
        'updated_at': post.updated_at.isoformat(),
        'image': post.image
    }

def delete_post(post_id, user_uid):
    try:
        post = Post.query.filter_by(uid=post_id).first()
        if not post:
            return {
                'message': 'Post not found',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40019'}
            }, 404

        if str(post.user_uid) != user_uid:
            return {
                'message': 'Unauthorized action',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40022'}
            }, 403

        db.session.delete(post)
        db.session.commit()
        return {
            'message': 'Post deleted successfully',
            'status': True,
            'type': 'success_message',
            'error_status': {'error_code': '00000'}
        }, 200
    except Exception as e:
        db.session.rollback()
        error_logger('delete_post', 'Failed to delete post', error=str(e), post_id=post_id)
        raise Exception("Database error")

# Comment Functions

def get_comment_by_comment_id(comment_id):
    try:
        comment = Comment.query.filter_by(uid=comment_id).first()
        return comment
    except Exception as e:
        error_logger('get_comment_by_comment_id', 'Comment not found', error=str(e), comment_id=comment_id)
        raise Exception("Database error")
    
def get_comments_by_post_id(post_uid):
    try:
        comments = Comment.query.filter_by(post_uid=post_uid).all()
        return comments
    except Exception as e:
        error_logger('get_comments_by_post_id', 'Failed to retrieve comments', error=str(e), post_uid=post_uid)
        raise Exception("Database error")

def create_new_comment(post_uid, user_uid, data, username):
    try:
        if 'uid' in data:
            new_comment = Comment(uid=data['uid'], content=data['content'], username=username, user_uid=user_uid, post_uid=post_uid)
        else:
            new_comment = Comment(content=data['content'], username=username, user_uid=user_uid, post_uid=post_uid)
        db.session.add(new_comment)
        db.session.commit()
        return new_comment
    except Exception as e:
        db.session.rollback()
        error_logger('create_new_comment', 'Failed to create comment', error=str(e), post_uid=post_uid, user_uid=user_uid, content=data['content'])
        raise Exception("Database error")

def update_existing_comment(comment,data):
    try:
        if data:
            comment.content = data.get('content', comment.content)
            db.session.commit()
            return True
        else:
            return False
    except Exception as e:
        db.session.rollback()
        error_logger('update_existing_comment', 'Failed to update comment', error=str(e))
        raise Exception("Database error")

def delete_existing_comment(comment):
    try:
      if comment:
          db.session.delete(comment)
          db.session.commit()
          return True
      else:
          return False
    except Exception as e:
        db.session.rollback()
        error_logger('delete_existing_comment', 'Failed to delete comment', error=str(e))
        raise Exception("Database error: ")


def get_paginated_posts(page, per_page, user_uid=None):
    try:
        page = int(page)
        per_page = int(per_page)

        offset = (page - 1) * per_page

        query = db.session.query(Post).order_by(desc(Post.created_at))

        if user_uid:
            query = query.filter(Post.user_uid == user_uid)

        total_posts = query.count()

        posts = query.offset(offset).limit(per_page).all()

        
        return posts, total_posts
    
    except Exception as e:
        error_logger('get_paginated_posts', 'Failed to retrieve posts', error=str(e), page=page, per_page=per_page, user_uid=user_uid)
        raise Exception("Database error")
