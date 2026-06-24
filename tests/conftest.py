import pytest
from flask import Flask
from app import create_app, db
from models import User, Post, Follow

@pytest.fixture(scope='module')
def app():
    app = create_app()
    with app.app_context():
        db.create_all()

    yield app

    with app.app_context():
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()