from flask import Blueprint, request, jsonify, session, redirect, url_for, render_template, flash
from functools import wraps

auth_blueprint = Blueprint('auth', __name__)

#Register users
@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    from app import mongo, bcrypt
    if request.method == 'POST':
        users = mongo.db.users
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role', 'user') #Standard role

        existing_user = users.find_one({'username': username})

        if existing_user is None:
            hashpass = bcrypt.generate_password_hash(password).decode('utf-8')
            users.insert_one({'username': username, 'password': hashpass, 'role': role})
            return jsonify(message="User registered successfully"), 201
        return jsonify(message="Username already exists"), 400
    return render_template('register.html')

#Login Users
@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    from app import mongo, bcrypt
    if request.method == 'POST':
        users = mongo.db.users
        username = request.form.get('username')
        password = request.form.get('password')

        user = users.find_one({'username': username})

        if user and bcrypt.check_password_hash(user['password'], password):
            session['username'] = username
            session['role'] = user['role']
            return jsonify(message="Logged in successfully"), 200
        return jsonify(message="Invalid credentials"), 401
    return render_template('login.html')

#Logout users
@auth_blueprint.route('/logout', methods=['GET'])
def logout():
    session.pop('username', None)
    return redirect(url_for('auth.login'))


#Admin requirement function
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'role' not in session or session['role'] != 'admin':
            flash("Admin access required")
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function