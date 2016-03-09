"""Application launcher."""
import concurrent.futures
import logging
import logging.handlers
import janrain_datalib
import marketorestpython.client
from janrain_marketo import create_app
from janrain_marketo.config import get_config
from janrain_marketo.lib import db

config = get_config()

janrain_app = janrain_datalib.get_app(
    config['JANRAIN_URI'],
    client_id=config['JANRAIN_CLIENT_ID'],
    client_secret=config['JANRAIN_CLIENT_SECRET'])
janrain_records = janrain_app.get_schema(config['JANRAIN_SCHEMA_NAME']).records

marketo_client = marketorestpython.client.MarketoClient(
    config['MARKETO_MUNCHKIN_ID'],
    client_id=config['MARKETO_CLIENT_ID'],
    client_secret=config['MARKETO_CLIENT_SECRET'])

executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)

# must be named application for beanstalk to find it automatically
application = create_app(config, janrain_records, marketo_client, executor)

# setup logging
handler = logging.handlers.RotatingFileHandler(
    config['APP_LOG_FILE'],
    backupCount=config['APP_LOG_NUM_BACKUPS'],
    maxBytes=config['APP_LOG_FILESIZE'])
if config['DEBUG']:
    handler.setLevel(logging.DEBUG)
else:
    handler.setLevel(logging.INFO)
msg_format = '[%(asctime)s] %(levelname)s: %(message)s'
timestamp_format = '%Y-%m-%d %H:%M:%S %z'
formatter = logging.Formatter(msg_format, timestamp_format)
handler.setFormatter(formatter)
logger = logging.getLogger(application.config['LOGGER_NAME'])
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

if __name__ == '__main__':
    # this is just for convenience during development
    if config['DEBUG'] and not db.JobsModel.exists():
        # create table with minimal capacity
        db.JobsModel.create_table(
            read_capacity_units=1,
            write_capacity_units=1,
        )
    application.run()
