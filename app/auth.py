import datetime
from flask import request, jsonify
from werkzeug.security import check_password_hash
from marshmallow import Schema, fields, validate, ValidationError
from functools import wraps
import jwt
from app import create_app
from models import User
import os

app = create_app()

# Configuración de JWT
SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
JWT_ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

def generate_token(user_id, expires_delta):
    payload = {
        'sub': user_id,
        'exp': datetime.datetime.utcnow() + expires_delta
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=JWT_ALGORITHM)

def decode_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload['sub']
    except jwt.ExpiredSignatureError:
        raise ValidationError('Token expired')
    except jwt.InvalidTokenError:
        raise ValidationError('Invalid token')

# Esquemas de validación
class LoginSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)

class RefreshSchema(Schema):
    refresh_token = fields.Str(required=True)

# Middleware para autenticación
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            user_id = decode_token(token)
            current_user = User.query.get(user_id)
            if not current_user:
                return jsonify({'message': 'User not found!'}), 401
            kwargs['current_user'] = current_user
        except ValidationError as e:
            return jsonify({'message': str(e)}), 403
        return f(*args, **kwargs)
    return decorated

# Endpoint de login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    try:
        LoginSchema().load(data)
    except ValidationError as err:
        return jsonify({'message': str(err)}), 400
    
    user = User.query.filter_by(username=data['username']).first()
    if not user or not check_password_hash(user.password_hash, data['password']):
        return jsonify({'message': 'Invalid credentials!'}), 401
    
    access_token_expires = datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = datetime.timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    
    access_token = generate_token(user.id, access_token_expires)
    refresh_token = generate_token(user.id, refresh_token_expires)
    
    # Aquí deberías almacenar el refresh token de alguna manera (por ejemplo, en una base de datos o cache)
    # Por simplicidad, no lo estamos haciendo aquí.
    
    return jsonify(access_token=access_token, refresh_token=refresh_token), 200

# Endpoint de refresh token
@app.route('/refresh', methods=['POST'])
def refresh():
    data = request.get_json()
    try:
        RefreshSchema().load(data)
    except ValidationError as err:
        return jsonify({'message': str(err)}), 400
    
    # Aquí deberías verificar el refresh token almacenado (por ejemplo, en una base de datos o cache)
    # Por simplicidad, no lo estamos haciendo aquí.
    
    try:
        user_id = decode_token(data['refresh_token'])
    except ValidationError as e:
        return jsonify({'message': str(e)}), 403
    
    access_token_expires = datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = generate_token(user_id, access_token_expires)
    
    return jsonify(access_token=access_token), 200

# Endpoint de logout
@app.route('/logout', methods=['POST'])
def logout():
    # Aquí deberías eliminar el refresh token almacenado (por ejemplo, en una base de datos o cache)
    # Por simplicidad, no lo estamos haciendo aquí.
    
    return jsonify({'message': 'Successfully logged out!'}), 200