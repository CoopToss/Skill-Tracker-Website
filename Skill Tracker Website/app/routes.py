from flask import redirect, url_for, render_template, request, flash, abort
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db
from app.models import User, Skill, Goal

@app.route('/')
def index():
    print("Inside index route")
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Retrieve form data
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

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
        print("Email:", email)
        print("Password:", password)

        # Find the user by email
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            # Log in the user
            login_user(user)
            print("User logged in successfully")

            # Redirect to the dashboard
            return redirect(url_for('dashboard'))
        else:
            # Authentication failed, render the login page with an error message
            print("Authentication failed")
            return render_template('login.html', error="Invalid email or password.")
    else:
        print("GET request received for login route")
        return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    user_id = current_user.id
    user = User.query.get(user_id)
    skills = Skill.query.filter_by(user_id=user_id).all()
    goals = Goal.query.filter_by(user_id=user_id).all()
    return render_template('dashboard.html', user=user, skills=skills, goals=goals)

@app.route('/add_skill', methods=['POST'])
def add_skill():
    if request.method == 'POST':
        # Retrieve skill data from the form
        skill_name = request.form.get('skill_name')
        hours_logged_str = request.form.get('hours_logged')
        goal_details = request.form.get('goal_details')

        # Check if hours_logged is not None and convert it to an integer
        if hours_logged_str is None:
            return redirect(url_for('dashboard'))  # Redirect if hours_logged is missing

        try:
            hours_logged = int(hours_logged_str)
        except ValueError:
            return redirect(url_for('dashboard'))  # Redirect if hours_logged is not a valid integer

        # Check if the skill already exists for the user
        existing_skill = Skill.query.filter_by(name=skill_name, user_id=current_user.id).first()
        
        if existing_skill:
            # Update the existing skill
            existing_skill.hours_logged += hours_logged
            existing_skill.goal_details = goal_details  # Optionally update goal details
        else:
            # Create a new Skill object with the goal as a string
            new_skill = Skill(name=skill_name, hours_logged=hours_logged, goal_details=goal_details, user_id=current_user.id)
            db.session.add(new_skill)
        
        db.session.commit()

        # Redirect the user to the dashboard or a relevant page
        return redirect(url_for('dashboard'))
    
@app.route('/skill/<int:skill_id>')
def skill_detail(skill_id):
    
    skill = Skill.query.get_or_404(skill_id)
   
    # Retrieve all goal details associated with the skill
    goal_details = [skill.goal_details] if skill.goal_details else []
    return render_template('skill_detail.html', skill=skill, goal_details=goal_details)

    # Handle invalid HTTP methods
    return redirect(url_for('dashboard'))

@app.route('/delete_skill/<int:skill_id>', methods=['POST'])

@login_required
def delete_skill(skill_id):
    skill = Skill.query.get_or_404(skill_id)
    # Check if the skill belongs to the current user
    if skill.user != current_user:
        abort(403)  # Forbidden
    db.session.delete(skill)
    db.session.commit()
    flash('Skill has been deleted!', 'success')
    return redirect(url_for('dashboard'))