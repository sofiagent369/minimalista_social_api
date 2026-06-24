from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import User, Post, Follow

db = SQLAlchemy()

def init_db():
    app = create_app()
    db.init_app(app)

    with app.app_context():
        db.create_all()
        # Crear usuarios iniciales (seeds)
        user1 = User(username='user1', email='user1@example.com', password_hash='hashed_password')
        user2 = User(username='user2', email='user2@example.com', password_hash='hashed_password')
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()

if __name__ == "__main__":
    init_db()