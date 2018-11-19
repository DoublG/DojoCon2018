from flask import Flask, g, current_app
from webhook.util import ApiLogin, RabbitMQ

login = ApiLogin()
rabbit = RabbitMQ()


def create_app(test_config=None, instance_relative_config=True):
    app = Flask(__name__)

    if test_config is None:
        app.config.from_object('webhook.default_settings')
        app.config.from_envvar('APP_SETTINGS', silent=True)
    else:
        app.config.update(test_config)

    login.init_app(app)
    rabbit.init_app(app)

    from . import views

    app.register_blueprint(views.app, url_prefix='/')

    return app
