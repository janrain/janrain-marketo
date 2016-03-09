"""Flask application setup."""
import flask
from janrain_marketo._version import __version__
from janrain_marketo.sync import start_sync

def create_app(config, janrain_records, marketo_client, executor):
    app = flask.Flask(__name__)
    app.config.update(config)

    @app.after_request
    def add_headers(response):
        """Additional headers for each response."""
        response.headers['X-App-Version'] = __version__
        return response

    # routes
    app.add_url_rule('/', 'root', lambda: 'ok')
    app.add_url_rule('/sync', 'sync', start_sync, methods=['POST'])

    # add objects to the app
    app.janrain_records = janrain_records
    app.marketo_client = marketo_client
    app.executor = executor

    return app
