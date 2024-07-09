from flask import Flask, flash, request, render_template, redirect, url_for, Blueprint
from flask_login import login_required, current_user
from .models import Note, db
from datetime import datetime

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template('index.html')

@views.route('/about')
def about():
    return render_template('about.html')

@views.route('/dashboard')
@login_required
def dashboard():
    return render_template('userDashboard.html')

@views.route('/notes')
@login_required
def notes():
    user_notes = Note.query.filter_by(userId=current_user.id).all()
    return render_template('notes.html', notes=user_notes)

@views.route('/addNote', methods=['POST'])
@login_required
def addNote():
    note_data = request.form.get('note_data')
    note_date_str = request.form.get('note_date')
    note_date = datetime.strptime(note_date_str, '%Y-%m-%d')
    new_note = Note(data=note_data, date=note_date, userId=current_user.id)
    db.session.add(new_note)
    db.session.commit()
    return redirect(url_for('views.notes'))

@views.route('/deleteNote/<int:note_id>', methods=['POST'])
@login_required
def deleteNote(note_id):
    note = Note.query.get(note_id)
    if note and note.userId == current_user.id:
        db.session.delete(note)
        db.session.commit()
    return redirect(url_for('views.notes'))