from flask import Flask, flash, request, render_template, redirect, url_for, Blueprint
from flask_login import login_required, current_user
from .models import Note, User, Project, Task, db
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

@views.route('/projects')
@login_required
def projects():
    if current_user.usertype != 'team_member':
        flash('Access denied. Only Team Members can view projects.', category='error')
        return redirect(url_for('views.dashboard'))
    
    userProjects = Project.query.filter_by(user_id=current_user.id).all()
    if not userProjects:
        return render_template('noProjects.html')
    return render_template('projectList.html', projects=userProjects)

@views.route('/addProject', methods=['GET', 'POST'])
@login_required
def addProject():
    if current_user.usertype != 'team_member':
        flash('Access denied. Only Team Members can add projects.', category='error')
        return redirect(url_for('views.dashboard'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        new_project = Project(name=name, description=description, user_id=current_user.id)
        db.session.add(new_project)
        db.session.commit()
        flash('Project added successfully!', category='success')
        return redirect(url_for('views.projects'))
    
    return render_template('addProject.html')

@views.route('/confirm-delete-project/<int:project_id>')
@login_required
def confirmDeleteProject(project_id):
    project = Project.query.get_or_404(project_id)
    if project.user_id != current_user.id:
        flash('You do not have permission to delete this project.', category='error')
        return redirect(url_for('views.projects'))
    return render_template('confirmDeleteProject.html', project=project)

@views.route('/delete-project/<int:project_id>', methods=['POST'])
@login_required
def deleteProject(project_id):
    project = Project.query.get_or_404(project_id)
    if project.user_id != current_user.id:
        flash('You do not have permission to delete this project.', category='error')
    else:
        db.session.delete(project)
        db.session.commit()
        flash('Project deleted successfully.', category='success')
    return redirect(url_for('views.projects'))