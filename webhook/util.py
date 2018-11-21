from flask_login import LoginManager, UserMixin
from flask import _app_ctx_stack as stack


class User(UserMixin):
    def __init__(self, name):
        self.id = name


class ApiLogin(object):
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.channel = None
            self.init_app(app)

    def init_app(self, app):
        login_manager = LoginManager(app)
        login_manager.init_app(app)

        @login_manager.request_loader
        def load_user_from_request(request):

            # http get
            api_key = request.args.get('api_key')

            # http headers
            if api_key is None:
                api_key = request.headers.get('X-API-Key')

            # cookies
            if api_key is None:
                api_key = request.cookies.get('X-API-KEY')

            if api_key != '' and api_key == app.config['API_KEY']:
                return User('api')

            app.logger.info('%s api key validation failed', api_key)
            return None


class RabbitMQ(object):
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def get_channel(self):
        import pika

        channel = getattr(stack.top, '_channel', None)

        if channel is None:
            credentials = pika.PlainCredentials(self.app.config['RABBITMQ_USER'], self.app.config['RABBITMQ_PWD'])

            connection = pika.BlockingConnection(pika.ConnectionParameters(
                host=self.app.config['RABBITMQ_HOST'], credentials=credentials))

            channel = connection.channel()
            channel.exchange_declare(exchange=self.app.config['RABBITMQ_EXCHANGE'],
                                     exchange_type=self.app.config['RABBITMQ_EXCHANGE_TYPE'])

            stack.top._channel = channel
            stack.top._connection = connection

        return channel

    def init_app(self, app):
        self.app = app

        @app.teardown_appcontext
        def teardown_connection(exception):
            connection = getattr(stack.top, '_connection', None)

            if connection is not None:
                connection.close()

    @property
    def channel(self):
        ctx = stack.top
        if ctx is not None:
            if not hasattr(ctx, '_channel'):
                ctx._channel = self.get_channel()
            return ctx._channel
