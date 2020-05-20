from flask import jsonify
from . import api
from app.models import User

@api.route('/users/')
def get_users():
    users = User.query.order_by(User.id).all()
    return jsonify([{'id':user.id,'info':user.to_json()} for user in users])

@api.route('/users/<int:id>')
def get_user(id):
    user = User.query.get_or_404(id)
    return  jsonify(user.to_json())

@api.route('/users/<int:id>/posts')
def get_user_posts(id):
    user = User.query.get_or_404(id)
    return jsonify([post.to_json() for post in user.posts])

@api.route('users/<int:id>/fllowed-posts')
def get_followed_posts(id):
    user = User.query.get_or_404(id)
    followed_ids = [f.followed_id for f in user.followed]
    followed = [User.query.get_or_404(followed_id)
            for followed_id in followed_ids
    ]
    return jsonify([
        { 'followed_id':u.id,
          'followed':u.name,
            'posts': [post.to_json() for post in u.posts] 
        }
          for u in followed
        ])
