from flask import Flask, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'change your key'  
jwt = JWTManager(app)

users = []

@app.route('/api/v1/user/login', methods=['POST'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')
    
    user = next((u for u in users if u['email'] == email), None)

    if user and check_password_hash(user['password'], password):
        access_token = create_access_token(identity=user['id'])  # Store the whole user object in the token
        return jsonify({'code': 0, 'data': access_token, 'msg': 'Login successful.'}), 200
    else:
        return jsonify({'code': 1, 'data': None, 'msg': 'Invalid email or password.'}), 400

@app.route('/api/v1/user/register', methods=['POST'])
def register():
    email = request.json.get('email')
    password = request.json.get('password')
    code = request.json.get('code')
    
    user = next((u for u in users if u['email'] == email), None)

    if user:
        return jsonify({'code': 1, 'data': None, 'msg': 'Email already registered.'}), 400
    elif code != '123456':  # Mock verification code
        return jsonify({'code': 1, 'data': None, 'msg': 'Invalid verification code.'}), 400
    else:
        hashed_password = generate_password_hash(password)
        new_user = {'id': len(users) + 1, 'email': email, 'password': hashed_password}
        users.append(new_user)
        return jsonify({'code': 0, 'data': new_user['id'], 'msg': 'Register successful.'}), 200

@app.route('/api/v1/user/profile', methods=['GET'])
@jwt_required()
def get_user_profile():
    user_id = get_jwt_identity()
    user = next((u for u in users if u['id'] == int(user_id)), None)
    if user:
        return jsonify({
            'code': 0,
            'data': {
                'id': user['id'],
                'email': user['email'],
                'integral': 66,
                'name': 'id'+str(user['id']),
            },
            'msg': 'Success.'
        }), 200
    else:
        return jsonify({'code': 1, 'data': None, 'msg': 'User not found.'}), 404

if __name__ == "__main__":
    app.run()