Janrain Marketo Connector
=========================

Overview
--------

Syncs records from Janrain to Marketo. Only records modified since the last time
the sync ran will be transferred on each run.


Configuration
-------------

The application reads its configuration from these environment variables:

- `DEBUG`: If this is set to anything other than empty string or the word
`FALSE`, then the app will run in debug mode. Additional info will be written
to the log.

- `APP_LOG_FILE`: Full path to the file where the app will write the log.
(should only be used during local development, leave blank when deployed
to elastic beanstalk)

- `APP_LOG_FILESIZE`: Maximum size in bytes of the app log before it gets
rotated. (default: `10000000`)

- `APP_LOG_NUM_BACKUPS`: Number of rotated backups of the app log that will
be kept. (default: `20`)

- `AWS_ACCESS_KEY_ID`: AWS key id to use.
(should only be used during local development, leave blank when deployed
to elastic beanstalk)

- `AWS_SECRET_ACCESS_KEY`: AWS secret to use.
(should only be used during
local development, leave blank when deployed to elastic beanstalk)

- `AWS_DEFAULT_REGION`: AWS region the app runs in.

- `AWS_DYNAMODB_URL`: Url of the DynamoDB service to use.
(should only be used during local development, leave blank when deployed
to elastic beanstalk)

- `AWS_DYNAMODB_TABLE`: Name of the table in DynamoDB to use.
(default: `janrain_marketo`)

* `JANRAIN_URI`: URI of the Janrain Capture app.

* `JANRAIN_CLIENT_ID`: Janrain API client to use.

* `JANRAIN_CLIENT_SECRET`: Secret for the client.

* `JANRAIN_SCHEMA_NAME`: Name of the Capture schema containing the user records.
(default: `user`)

* `JANRAIN_BATCH_SIZE_LIMIT`: Max number of records to retrieve from Janrain
at a time.
(default: `1000`)

* `JANRAIN_MARKETO_FIELD_MAP`: Must be a string that decodes to a JSON object
that maps Janrain fields to Marketo fields.
(default: `{"email": "email", "uuid": "janrainUUID"}`)

* `MARKETO_CLIENT_ID`: Marketo API client to use.

* `MARKETO_CLIENT_SECRET`: Secret for the client.

* `MARKETO_MUNCHKIN_ID`: The Marketo Munchkin ID, also the first part of the
domain for the Marketo API.

* `MARKETO_BATCH_SIZE_LIMIT`: Max number of records to send to Marketo
at a time.
(default: `300`)

- `DB_UPDATE_INTERVAL`: Number of seconds between recording status updates to
the db.
(default: `10`)


Maintenance
-----------

When deployed to Elastic Beanstalk, the application log is shipped to
Cloudwatch Logs.


Development
-----------

To run the app locally:

1. Setup a python 3 virtual env and install libaries: 
`pyvenv venv; source venv/bin/activate; pip install -r requirements.txt`
2. [Download](http://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Tools.DynamoDBLocal.html) and start a local instance of DynamoDB
3. Set the environment variable `AWS_DYNAMODB_URL` to point to the local 
DynamoDB instance (`http://localhost:8000` by default)
4. Create and source a `env.sh` file that exports the environment variables the app needs
5. Run the app: `python application.py`


QA
--

1. Run nose `nosetests`
