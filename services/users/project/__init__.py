import os
import datetime
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension

"""Creates a Flask App"""


# Instantiate db
db = SQLAlchemy()
migrate = Migrate()
toolbar = DebugToolbarExtension()

def create_app(script_info=None):

    app = Flask(__name__)

    # enable CORS
    CORS(app)

    # set config
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)

    # set up extensions
    db.init_app(app)
    toolbar.init_app(app)
    migrate.init_app(app, db)

    # register blueprints
    from project.api.users import users_blueprint
    app.register_blueprint(users_blueprint)

    app.shell_context_processor({'app': app, 'db': db})
    return app