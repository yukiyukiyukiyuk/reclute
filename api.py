from flask import Flask, request, jsonify
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
auth = HTTPBasicAuth()

# ユーザ情報の格納先 (仮のデータベース)
users = {
    "TaroYamada": {
        "user_id": "TaroYamada",
        "password": "PaSSwd4TY",
        "nickname": "たろー!",
        "comment": "僕は元気です！"
    }
}

@auth.verify_password
def verify_password(username, password):
    if username in users:
        if password == users[username]["password"]:
            return username

@auth.error_handler
def unauthorized():
    return jsonify({"message": "Authentication Failed"}), 401

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the API"}), 200

@app.route('/favicon.ico')
def favicon():
    return "", 204

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    user_id = data.get('user_id')
    password = data.get('password')

    if not user_id or not password:
        return jsonify({"message": "Account creation failed", "cause": "required user_id and password"}), 400

    if user_id in users:
        return jsonify({"message": "Account creation failed", "cause": "already same user_id is used"}), 400

    # ユーザ情報を作成
    user = {
        "user_id": user_id,
        "password": password,
        "nickname": user_id,
        "comment": ""
    }
    users[user_id] = user

    return jsonify({"message": "Account successfully created", "user": user}), 200

@app.route('/users/<user_id>', methods=['GET'])
@auth.login_required
def get_user(user_id):
    if user_id not in users:
        return jsonify({"message": "No User found"}), 404

    user = users[user_id]
    return jsonify({"message": "User details by user_id", "user": user}), 200

@app.route('/users/<user_id>', methods=['PATCH'])
@auth.login_required
def update_user(user_id):
    if user_id not in users:
        return jsonify({"message": "No User found"}), 404

    data = request.get_json()
    nickname = data.get('nickname')
    comment = data.get('comment')

    if not nickname and not comment:
        return jsonify({"message": "User updation failed", "cause": "required nickname or comment"}), 400

    if 'user_id' in data or 'password' in data:
        return jsonify({"message": "User updation failed", "cause": "not updatable user_id and password"}), 400

    user = users[user_id]
    if nickname:
        user["nickname"] = nickname
    if comment:
        user["comment"] = comment

    return jsonify({"message": "User successfully updated", "user": user}), 200

@app.route('/close', methods=['POST'])
@auth.login_required
def close_account():
    user_id = auth.current_user()

    if user_id not in users:
        return jsonify({"message": "No User found"}), 404

    del users[user_id]
    return jsonify({"message": "Account and user successfully removed"}), 200

if __name__ == '__main__':
    app.run(host="34.84.134.241", debug=False)
