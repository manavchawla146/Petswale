from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .models import User

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['POST'])
def login():
    # Get form data
    email = request.form.get('email')
    password = request.form.get('password')
    
    # Find user by email
    user = User.query.filter_by(email=email).first()
    
    # Check if user exists and password is correct
    if not user or not user.verify_password(password):
        flash('Please check your login details and try again.')
        return redirect(url_for('main.signin'))
    
    # If validation passes, log in the user
    login_user(user)
    
    # Redirect based on admin status
    if user.is_admin:
        return redirect(url_for('admin.index'))  # Changed to use url_for with admin blueprint
    return redirect(url_for('main.home'))

@auth.route('/register', methods=['POST'])
def register():
    # Get form data
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    
    # Check if user already exists
    email_exists = User.query.filter_by(email=email).first()
    username_exists = User.query.filter_by(username=name).first()
    
    if email_exists:
        flash('Email already exists.')
        return redirect(url_for('main.signin'))
    
    if username_exists:
        flash('Username already exists.')
        return redirect(url_for('main.signin'))
    
    # Create new user
    new_user = User(
        username=name,
        email=email,
        password=password  # This will use the password setter to hash the password
    )
    
    # Add user to database
    db.session.add(new_user)
    db.session.commit()
    
    # Log in the new user
    login_user(new_user)
    return redirect(url_for('main.home'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))