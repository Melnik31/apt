from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, current_user, logout_user

main_bp = Blueprint('main', __name__)

@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']

        # Check if the username or email already exists
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            flash('Username or email already exists', 'error')
            return redirect(url_for('main.register'))
        # Create a new user
        new_user = User(
            username=username, 
            email=email, 
            password_hash=generate_password_hash(password), 
            role=role)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('main.register'))
        
    #Get request
    return render_template('register.html')

@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    # login logic
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the user exists
        user = User.query.filter_by(username=username).first()
        # if not found or password is incorrect, flash an error message, redirect to login page
        if not user or not check_password_hash(user.password_hash, password):
            flash('Invalid username or password', 'error')
            return redirect(url_for('main.login'))
        # if user is found and password is correct, log the user in and redirect to dashboard
        login_user(user)
        flash('Login successful!', 'success')
        return redirect(url_for('main.dashboard'))
        
    return render_template('login.html')

@main_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('main.login'))

@main_bp.route('/dashboard')
@login_required
def dashboard():
    # dashboard logic
    if current_user.role == 'coach':
        return redirect(url_for('main.coach_dashboard'))
    return redirect(url_for('main.athlete_dashboard'))

@main_bp.route('/athlete/dashboard')
@login_required
def athlete_dashboard():
    # athlete dashboard logic
    return render_template('athlete_dashboard.html')

@main_bp.route('/coach/dashboard')
@login_required
def coach_dashboard():
    # coach dashboard logic
    return render_template('coach_dashboard.html')
    
        