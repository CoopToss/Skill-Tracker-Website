from flask import redirect, url_for, render_template, request
from flask_login import login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import app, db
from app.models import User

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Retrieve form data
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        password_encoded = request.form.get('password')
        password_encoded = password_encoded.encode("utf-8", "ignore")  # Decode the password

        # Create a new user
        new_user = User(username=username, email=email)
        new_user.set_password(password)  # Set the password hash

        # Add the user to the database
        db.session.add(new_user)
        db.session.commit()

        # Log in the new user
        login_user(new_user)

        # Redirect to the dashboard
        return redirect(url_for('dashboard'))
    else:
        return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Find the user by email
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            # Log in the user
            login_user(user)

            # Redirect to the dashboard
            return redirect(url_for('dashboard'))
        else:
            # Authentication failed, render the login page with an error message
            return render_template('login.html', error="Invalid email or password.")
    else:
        return render_template('login.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    # Ensure the user is authenticated
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    return render_template('dashboard.html')