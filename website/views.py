from flask import Flask, flash, request, render_template, redirect, url_for, Blueprint
from flask_login import login_required, current_user

import json
import csv

views = Blueprint('views', __name__)

@views.route('/')
# @login_required
def home():
    return render_template('index.html')

@views.route('/about')
def about():
    return render_template('about.html')
@views.route('/dashboard')
@login_required
def dashboard():
    return render_template('userDashboard.html')