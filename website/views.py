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

@views.route('/tasks')
@login_required
def tasks():
    user_tasks = Task.query.filter_by(user_id=current_user.id).all()
    if not user_tasks:
        return render_template('noTasks.html')
    return render_template('taskList.html', tasks=user_tasks)

@views.route('/task/<int:task_id>')
@login_required
def task_detail(task_id):
    task = Task.query.get_or_404(task_id)
    project = Project.query.get(task.project_id)
    if project.user_id != current_user.id:
        flash('You do not have permission to view this task.', category='error')
        return redirect(url_for('views.tasks'))
    return render_template('taskDetail.html', task=task)

@views.route('/editTask/<int:task_id>', methods=['GET', 'POST'])
@login_required
def editTask(task_id):
    task = Task.query.get_or_404(task_id)
    if task.project.user_id != current_user.id:
        flash('You do not have permission to edit this task.', category='error')
        return redirect(url_for('views.tasks'))
    
    users = User.query.filter(User.usertype != 'viewer').all()  # Query users

    if request.method == 'POST':
        task.name = request.form.get('name')
        task.description = request.form.get('description')
        task.status = request.form.get('status')
        assigned_personnel_id = request.form.get('assigned_personnel')
        task.assigned_personnel_id = assigned_personnel_id  # Update assigned personnel
        db.session.commit()
        flash('Task updated successfully!', category='success')
        return redirect(url_for('views.task_detail', task_id=task.id))
    
    return render_template('editTask.html', task=task, users=users)

@views.route('/delete-task/<int:task_id>', methods=['POST'])
@login_required
def deleteTask(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        flash('You do not have permission to delete this task.', category='error')
    else:
        db.session.delete(task)
        db.session.commit()
        flash('Task deleted successfully.', category='success')
    return redirect(url_for('views.tasks'))

@views.route('/download_tasks_csv')
@login_required
def download_tasks_csv():
    import csv
    from io import StringIO
    from flask import make_response

    user_tasks = Task.query.filter_by(user_id=current_user.id).all()

    si = StringIO()
    cw = csv.writer(si)
    cw.writerow(['Task Name', 'Description', 'Status'])
    for task in user_tasks:
        cw.writerow([task.name, task.description, task.status])

    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=tasks.csv"
    output.headers["Content-type"] = "text/csv"
    return output

@views.route('/project/<int:project_id>/tasks')
@login_required
def project_tasks(project_id):
    project = Project.query.get_or_404(project_id)
    if project.user_id != current_user.id:
        flash('You do not have permission to view tasks for this project.', category='error')
        return redirect(url_for('views.projects'))
    
    tasks = Task.query.filter_by(project_id=project_id).all()
    return render_template('taskList.html', tasks=tasks, project=project)

@views.route('/edit-project/<int:project_id>', methods=['GET', 'POST'])
@login_required
def editProject(project_id):
    project = Project.query.get_or_404(project_id)
    if project.user_id != current_user.id:
        flash('You do not have permission to edit this project.', category='error')
        return redirect(url_for('views.projects'))

    if request.method == 'POST':
        project.name = request.form.get('name')
        project.description = request.form.get('description')
        db.session.commit()
        flash('Project updated successfully!', category='success')
        return redirect(url_for('views.projects'))

    return render_template('editProject.html', project=project)

@views.route('/addTask/<int:project_id>', methods=['GET', 'POST'])
@login_required
def addTask(project_id):
    project = Project.query.get_or_404(project_id)
    if current_user.usertype != 'team_member':
        flash('Access denied. Only Team Members can add tasks.', category='error')
        return redirect(url_for('views.projects'))
    
    users = User.query.filter(User.usertype != 'viewer').all()
    
    if request.method == 'POST':
        name = request.form.get('name')
        assigned_personnel_id = request.form.get('assigned_personnel')
        due_date = request.form.get('due_date')
        description = request.form.get('description')
        priority = request.form.get('priority')
        progress = request.form.get('progress')
        
        new_task = Task(
            name=name,
            description=description,
            status='Not Started',
            priority=priority,
            progress=progress,
            project_id=project_id
        )
        db.session.add(new_task)
        db.session.commit()
        flash('Task added successfully!', category='success')
        return redirect(url_for('views.projects'))
    
    return render_template('addTask.html', project=project, users=users)

@views.route('/project/<int:project_id>/tasks')
@login_required
def projectTasks(project_id):
    project = Project.query.get_or_404(project_id)
    if project.user_id != current_user.id:
        flash('You do not have permission to view tasks for this project.', category='error')
        return redirect(url_for('views.projects'))
    
    tasks = Task.query.filter_by(project_id=project_id).all()
    if not tasks:
        return render_template('noTasksForProject.html', project=project)
    
    return render_template('taskList.html', project=project, tasks=tasks)