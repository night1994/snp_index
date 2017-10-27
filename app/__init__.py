from flask import Flask
from settings import config


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    from .main import main as main_blueprint
    from .tools import tools as tools_blueprint
    app.register_blueprint(main_blueprint)
    app.register_blueprint(tools_blueprint)

    return app