
"""
Authentication Blueprint

NOTE: A Blueprint is a way to orgnaize a group of related views and other code. Rather  
than registering views and other code directly with an application, they are registered 
with a blueprint. Then the blueprint is registered with the application when it is available
in the factory function
"""
import functools
import re

from flask import(
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from app.mod_auth.forms import LoginForm, RegisterForm
from app.mod_auth.models import User
from app.db import db_session

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST')) #/auth/register
def register():
    """
    If user submitted the form, request.method will be POST so inputs gets validated,
    otherwise, it will just render the register.htmnl page
    """
    form = None
    if request.method == 'POST':
        form = RegisterForm(request.form)
        if form.validate():
            user = User.query.filter_by(username=form.username.data).first()
            if not user:
                db_session.add(User(form.username.data, generate_password_hash(form.password.data)))
                db_session.commit()
                flash(f"User ({user}) successfully regsitered to the system!")
                return redirect(url_for(('index')))

            flash('User is already registered', 'error-message')
        return redirect(url_for("auth.login"))

    return render_template('auth/register.html', form=form)

@bp.route('/login', methods=('GET', 'POST'))
def login():
    """
    If user submitted the form, request.method will be POST so inputs gets validated,
    otherwise, it will just render the login.htmnl page. 
    
    If validation is successful a session dict is created which stores data across requests.
    The data is stored in a cookie that is sent to the browser, and the browser then sends 
    it back with subsequent requests. Flask securely signs the data sot aht it can't be tampered with.
    """
    form = None
    if request.method == 'POST':
        form = LoginForm(request.form)
        if form.validate():
            user = User.query.filter_by(username=form.username.data).first()
            if user and check_password_hash(user.password, form.password.data):
                session['user_id'] = user.id
                flash(f'Welcome {user.username}')
                return redirect(url_for(('index')))
            flash('Wrong username or passowrd', 'error-message')
    return render_template('auth/login.html', form=form)

@bp.before_app_request
def load_logged_in_user():
    """
    Middleware (i.e., registered function that runs before the view function no matter
    which URL is requested). CHecks if user id is stored in the session and fetches users
    data from the database, storing it on g.user, which lasts for the length of request.
    """
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.filter_by(id=user_id).first()

def login_required(view):
    """ Checks if user is loaded and redirects ot the login page otherwise 
    If user is loaded the original view is called and continnues normally. """
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view

@bp.route('/logout')
def logout():
    """ Removes user_id form the session. """
    session.clear()
    return redirect(url_for('index'))