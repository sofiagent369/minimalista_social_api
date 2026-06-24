import pytest
from models import User, Follow

def test_add_follow(client):
    user1 = User(username='user1', email='user1@example.com', password_hash='hashed_password')
    user2 = User(username='user2', email='user2@example.com', password_hash='hashed_password')
    client.post('/login', json={'username': 'user1', 'password': 'password'})
    
    response = client.post('/follows', json={'follower_id': 1, 'followed_id': 2})
    assert response.status_code == 201
    assert response.json['follower_id'] == 1
    assert response.json['followed_id'] == 2

def test_get_follows(client):
    user1 = User(username='user1', email='user1@example.com', password_hash='hashed_password')
    user2 = User(username='user2', email='user2@example.com', password_hash='hashed_password')
    follow = Follow(follower_id=1, followed_id=2)
    client.post('/login', json={'username': 'user1', 'password': 'password'})
    
    response = client.get('/follows')
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_delete_follow(client):
    user1 = User(username='user1', email='user1@example.com', password_hash='hashed_password')
    user2 = User(username='user2', email='user2@example.com', password_hash='hashed_password')
    follow = Follow(follower_id=1, followed_id=2)
    client.post('/login', json={'username': 'user1', 'password': 'password'})
    
    response = client.delete(f'/follows/{follow.id}')
    assert response.status_code == 200
    assert response.json['message'] == 'Follow deleted!'