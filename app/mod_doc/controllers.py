import os


from pathlib import Path
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session, current_app
)
from app.mod_auth.controllers import login_required

bp = Blueprint('doc', __name__)

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'pdf', 'gif'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/')
def index():
    """ Renders index HTML page"""
    return render_template('index.html', docs=None)
    

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        if not title:
            error = 'Title is required.'
        
        file = None
        if 'file' not in request.files:
            flash('Missing file part')
            return redirect(request.url)
        else:
            file = request.files['file']
    
        if file.filename == '':
            flash('No file selected for upload')
            return redirect(request.url)
        elif file and not allowed_file(file.filename):
            flash('File extension is NOT supported!')
            return redirect(request.url)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO document (title, author_id, template)'
                ' VALUES (?, ?, ?)',
                (title, g.user['id'], file.read())
            )
            db.commit()
            return redirect(url_for('document.index'))

    return render_template('document/create.html')
