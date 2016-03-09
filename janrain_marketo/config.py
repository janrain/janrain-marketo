"""Application configuration"""
import json
import os

# environment variables and their defaults if empty or not defined
ENV_VARS = {
    'DEBUG': False,
    'APP_LOG_FILE': '/opt/python/log/application.log',
    'APP_LOG_FILESIZE': 10000000,
    'APP_LOG_NUM_BACKUPS': 20,
    'AWS_ACCESS_KEY_ID': '',
    'AWS_SECRET_ACCESS_KEY': '',
    'AWS_DEFAULT_REGION': '',
    'AWS_DYNAMODB_URL': None,
    'AWS_DYNAMODB_TABLE': 'janrain_marketo',
    'JANRAIN_URI': '',
    'JANRAIN_CLIENT_ID': '',
    'JANRAIN_CLIENT_SECRET': '',
    'JANRAIN_SCHEMA_NAME': 'user',
    'JANRAIN_BATCH_SIZE_LIMIT': 1000,
    'JANRAIN_MARKETO_FIELD_MAP': {
        'uuid': 'janrainUUID',
        'email': 'email',
    },
    'MARKETO_CLIENT_ID': '',
    'MARKETO_CLIENT_SECRET': '',
    'MARKETO_MUNCHKIN_ID': '',
    'MARKETO_BATCH_SIZE_LIMIT': 300,
    'DB_UPDATE_INTERVAL': 10,
}

def get_config():
    config = {}
    for key, default_value in ENV_VARS.items():
        value = os.getenv(key, '')
        # empty string means use default value
        if value == '':
            value = default_value
        elif isinstance(ENV_VARS[key], bool):
            if value.upper() != 'FALSE':
                value = True
            else:
                value = False
        elif isinstance(ENV_VARS[key], int):
            try:
                value = int(value)
            except ValueError:
                value = default_value
        elif isinstance(ENV_VARS[key], (dict, list)):
            try:
                value = json.loads(value)
            except ValueError:
                value = default_value
        config[key] = value
    return config
