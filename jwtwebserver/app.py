from flask import Flask, request, jsonify, render_template, redirect, url_for
import jwt
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super_secret_key'  # 실제 배포 시 환경 변수로 관리하세요.

# ✅ 루트 페이지 (로그인 페이지로 리디렉션)
@app.route('/')
def home():
    return redirect(url_for('login_page'))

# ✅ 로그인 페이지
@app.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')

# ✅ 로그인 요청 (POST)
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # 단순 예시 — 실제로는 DB 검증 필요
    if username == 'admin' and password == '1234':
        token = jwt.encode({
            'user': username,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=1)
        }, app.config['SECRET_KEY'], algorithm='HS256')

        return jsonify({'token': token})
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

# ✅ 보호된 페이지 (HTML)
@app.route('/protected', methods=['GET'])
def protected_page():
    return render_template('protected.html')

# ✅ 보호된 API (JWT 검증)
@app.route('/api/protected', methods=['GET'])
def protected():
    token = request.headers.get('Authorization')

    if not token:
        return jsonify({'message': 'Token is missing!'}), 401

    try:
        # Bearer 접두어 제거
        token = token.replace('Bearer ', '')
        decoded = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return jsonify({'message': f"Welcome, {decoded['user']}! You accessed a protected route."})
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token expired!'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid token!'}), 401


if __name__ == '__main__':
    app.run(port=4200, debug=True)
