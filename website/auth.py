from flask import Flask, flash, request, render_template, redirect, url_for, Blueprint
from .models import User
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

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                # login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect credentials.', category='error')
        else:
            flash('Username not found.', category='error')
    return render_template('login.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/registerAuth', methods=['GET', 'POST'])
def registerAuth():
    if request.method == 'POST':
        user_passcode = request.form.get('passcode', '')
        user_password = request.form.get('password', '')
        #if totp.verify(str(user_passcode)) or user_passcode == 1234 and user_password == correctPassword:
        if user_password == correctPassword:
            return render_template('register.html')
        elif user_password == "english>maths":
            flash("No, it's not!", category='error')
        else:
            flash("Incorrect combination.", category='error')
    return render_template('registerAuthorise.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        usertype = request.form.get('user-type')

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
            return redirect(url_for('auth.login'))

    users = User.query.all()
    print(users)
    return render_template('register.html', users=users)

@auth.route('/user/<int:user_id>')
def user_profile(user_id):
    user = User.query.get(user_id)
    if user:
        # Render user profile template or return user details
        return render_template('user_profile.html', user=user)
    else:
        flash('User not found', category='error')
        return redirect(url_for('auth.register'))

