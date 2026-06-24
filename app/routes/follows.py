from flask import request, jsonify
from app import create_app
from models import Follow, db
from schemas.follow_schema import FollowSchema

app = create_app()
follow_schema = FollowSchema()
follows_schema = FollowSchema(many=True)

@app.route('/follows', methods=['POST'])
def add_follow():
    data = request.get_json()
    try:
        follow_data = follow_schema.load(data)
    except Exception as err:
        return jsonify({'message': str(err)}), 400
    
    new_follow = Follow(follower_id=follow_data['follower_id'], followed_id=follow_data['followed_id'])
    
    db.session.add(new_follow)
    db.session.commit()
    
    return follow_schema.jsonify(new_follow), 201

@app.route('/follows', methods=['GET'])
def get_follows():
    all_follows = Follow.query.all()
    result = follows_schema.dump(all_follows)
    return jsonify(result)

@app.route('/follows/<id>', methods=['DELETE'])
def delete_follow(id):
    follow = Follow.query.get_or_404(id)
    db.session.delete(follow)
    db.session.commit()
    
    return jsonify({'message': 'Follow deleted!'})