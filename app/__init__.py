from flask import Flask

from config import Config
from app.extensions import db, socketio

def create_app(config_class=Config):
    app = Flask(__name__)


    app.config.from_object(config_class)

    # Initialized Flask Extension here
    db.init_app(app)
    socketio.init_app(app)

    # Register blueprints here
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    return app
