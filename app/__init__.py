import os

from app.db import db_session
from flask import Flask, render_template

from app.mod_auth import controllers

def create_app(test_config=None):
    """
    Instead of creating Flask instance globally, we will create it inside a function. 
    This function is known as the application factory. Any configuration, registration,
    and other setup the application needs will happen inside the function, then the 
    application will be returned (i.e., initialized)
    
    :param test_config (defualt None) - configuration to test
    :return instance of flask.Flask class
    """
    # __name__ is the name of the current Python module and the app needs it in order to know where its located to setup some paths
    # instance_relative_config = True tells the app that configuration files ar erelative to the instance folder - instance folder
    # is located outside the docgen package and can hold local data that shouldnt be commited to version control such as config secrets
    # and database file.
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        UPLOAD_FOLDER='static/images',
    )

    if test_config is None:
        # Load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Load the test config if passed as an function argument
        app.config.from_mapping(test_config)

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass    
    
    from app.db import init_db
    init_db()

    @app.route('/')
    def index():
        """ Renders index HTML page"""
        return render_template('index.html', docs=None)

    from app.mod_auth.controllers import bp as auth_bp
    app.register_blueprint(auth_bp)

    from app.mod_doc.controllers import bp as doc_bp
    app.register_blueprint(doc_bp)
    # Associates endpoint name (in this case 'index') with '/' url, so that url_for('index') and 
    # url_for('docgen.index') will both get same URL ether way
    app.add_url_rule('/', endpoint='index')
    
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()
        
    return app