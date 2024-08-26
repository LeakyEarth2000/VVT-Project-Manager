from flask import Flask, flash, request, render_template, redirect, url_for, Blueprint, abort
from .models import User
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, current_user, logout_user
import json
import csv
import random
import string
from twofactorauth import totp

auth = Blueprint('auth', __name__)

# makes this work everywhere in the code
global correctPassword
correctPassword = "Ilovepython"
print(correctPassword)

def VVT_Admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_anonymous or current_user.username != 'VVT_Admin':
            abort(403)  # Forbidden
        return f(*args, **kwargs)
    return decorated_function

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True) 
                return redirect(url_for('views.dashboard'))
            else:
                flash('Incorrect credentials.', category='error')
        else:
            flash('Username not found.', category='error')
    return render_template('login.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.home'))


@auth.route('/registerAuth', methods=['GET', 'POST'])
def registerAuth():
    if request.method == 'POST':
        user_passcode = request.form.get('passcode', '')
        user_password = request.form.get('password', '')
        if totp.verify(str(user_passcode)) or user_passcode == 1234 and user_password == correctPassword:
            # create a temporary user object for the session
            VVT_Admin = User.query.filter_by(username='VVT_Admin').first()
            if not VVT_Admin:
                VVT_Admin = User(username='VVT_Admin', password=generate_password_hash(correctPassword, method='pbkdf2:sha256'))
                db.session.add(VVT_Admin)
                db.session.commit()
            login_user(VVT_Admin)
            return redirect(url_for('auth.register'))
        elif user_password == "english>maths":
            flash("No, it's not!", category='error')
        else:
            flash("Incorrect combination.", category='error')
    return render_template('registerAuthorise.html')

@auth.route('/register', methods=['GET', 'POST'])
@login_required
@VVT_Admin_required
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        usertype = request.form.get('usertype')

        user = User.query.filter_by(username=username).first()
        if user:
            flash(f'Username {username} already exists.', category='error')
        elif username is None or len(username) < 3:
            flash('Username must be greater than 2 characters.', category='error')
        elif password is None or len(password) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(username=username, password=generate_password_hash(
                password, method='pbkdf2:sha256'), usertype=usertype)
            db.session.add(new_user)
            db.session.commit()
            flash('Account created! Please login', category='success')
            return redirect(url_for('auth.register'))

    # Fetch all users from the database
    users = User.query.all()
    print("Fetched users:", users)
    return render_template('register.html', users=users)

@auth.route('/user/<int:user_id>')
@login_required
@VVT_Admin_required
def userProfile(user_id):
    user = User.query.get(user_id)
    if user:
        # Render user profile template with the user object
        return render_template('userProfile.html', user=user)
    else:
        flash('User not found', category='error')
        return redirect(url_for('auth.register'))

@auth.route('/user/<int:user_id>/change-password', methods=['POST'])
@login_required
@VVT_Admin_required
def changePassword(user_id):
    user = User.query.get(user_id)
    if user:
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        if new_password != confirm_password:
            flash('Passwords do not match.', category='error')
        elif len(new_password) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            user.password = generate_password_hash(new_password, method='pbkdf2:sha256')
            db.session.commit()
            flash('Password changed successfully.', category='success')
    else:
        flash('User not found', category='error')
    
    return redirect(url_for('auth.userProfile', user_id=user_id))

@auth.route('/user/<int:user_id>/delete', methods=['POST'])
@login_required
@VVT_Admin_required
def deleteUser(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        flash('User deleted successfully', category='success')
    else:
        flash('User not found', category='error')
    return redirect(url_for('auth.register'))

@auth.route('/confirmDelete/<int:user_id>', methods=['GET', 'POST'])
@login_required
@VVT_Admin_required
def confirmDelete(user_id):
    user = User.query.get(user_id)
    if user:
        return render_template('confirmDelete.html', user=user)
    else:
        flash('User not found', category='error')
        return redirect(url_for('auth.register'))