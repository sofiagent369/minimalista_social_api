from flask import request, jsonify
from app import create_app
from models import Post, db
from schemas.post_schema import PostSchema
import os

app = create_app()
post_schema = PostSchema()
posts_schema = PostSchema(many=True)

@app.route('/posts', methods=['POST'])
def add_post():
    data = request.get_json()
    try:
        post_data = post_schema.load(data)
    except Exception as err:
        return jsonify({'message': str(err)}), 400
    
    new_post = Post(content=post_data['content'], user_id=data['user_id'])
    
    db.session.add(new_post)
    db.session.commit()
    
    return post_schema.jsonify(new_post), 201

@app.route('/posts', methods=['GET'])
def get_posts():
    all_posts = Post.query.all()
    result = posts_schema.dump(all_posts)
    return jsonify(result)

@app.route('/posts/<id>', methods=['GET'])
def get_post(id):
    post = Post.query.get_or_404(id)
    return post_schema.jsonify(post)

@app.route('/posts/<id>', methods=['PUT'])
def update_post(id):
    data = request.get_json()
    try:
        post_data = post_schema.load(data)
    except Exception as err:
        return jsonify({'message': str(err)}), 400
    
    post = Post.query.get_or_404(id)
    
    post.content = post_data['content']
    db.session.commit()
    
    return post_schema.jsonify(post)

@app.route('/posts/<id>', methods=['DELETE'])
def delete_post(id):
    post = Post.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    
    return jsonify({'message': 'Post deleted!'})