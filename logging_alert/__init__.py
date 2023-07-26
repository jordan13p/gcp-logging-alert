from flask import Flask
from .controllers import logging_alert

def init_app():
    app = Flask(__name__)

    # Register Blueprints
    app.register_blueprint(logging_alert.logging_alert_bp)

    return app
