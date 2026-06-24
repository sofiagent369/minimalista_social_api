import pytest
from models import User, Post

def test_add_post(client):
    user = User(username='testuser', email='test@example.com', password_hash='hashed_password')
    client.post('/login', json={'username': 'testuser', 'password': 'password'})
    
    response = client.post('/posts', json={'content': 'Test post content', 'user_id': 1})
    assert response.status_code == 201
    assert response.json['content'] == 'Test post content'

def test_get_posts(client):
    user = User(username='testuser', email='test@example.com', password_hash='hashed_password')
    client.post('/login', json={'username': 'testuser', 'password': 'password'})
    
    response = client.get('/posts')
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_get_post(client):
    user = User(username='testuser', email='test@example.com', password_hash='hashed_password')
    post = Post(content='Test post content', user_id=1)
    client.post('/login', json={'username': 'testuser', 'password': 'password'})
    
    response = client.get(f'/posts/{post.id}')
    assert response.status_code == 200
    assert response.json['content'] == 'Test post content'

def test_update_post(client):
    user = User(username='testuser', email='test@example.com', password_hash='hashed_password')
    post = Post(content='Test post content', user_id=1)
    client.post('/login', json={'username': 'testuser', 'password': 'password'})
    
    response = client.put(f'/posts/{post.id}', json={'content': 'Updated test post content', 'user_id': 1})
    assert response.status_code == 200
    assert response.json['content'] == 'Updated test post content'

def test_delete_post(client):
    user = User(username='testuser', email='test@example.com', password_hash='hashed_password')
    post = Post(content='Test post content', user_id=1)
    client.post('/login', json={'username': 'testuser', 'password': 'password'})
    
    response = client.delete(f'/posts/{post.id}')
    assert response.status_code == 200
    assert response.json['message'] == 'Post deleted!'