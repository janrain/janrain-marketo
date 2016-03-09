# -*- coding: utf-8 -*-
import tempfile
import unittest
import unittest.mock
from janrain_marketo import create_app
from janrain_marketo.config import get_config

class ApiTests(unittest.TestCase):

    def setUp(self):
        self.logfile = tempfile.NamedTemporaryFile()
        config = get_config()
        config['APP_LOG_FILE'] = self.logfile.name

        self.janrain_app = unittest.mock.MagicMock()
        self.marketo_client = unittest.mock.MagicMock()
        self.executor = unittest.mock.MagicMock()

        app = create_app(config, self.janrain_app, self.marketo_client, self.executor)
        app.testing = True
        self.app = app.test_client()

    def tearDown(self):
        self.logfile.close()

    def test_root(self):
        r = self.app.get('/')
        self.assertEqual(r.status_code, 200)

    def test_sync(self):
        with unittest.mock.patch('janrain_marketo.sync.db') as db:
            r = self.app.post('/sync')
            self.assertEqual(r.status_code, 200)
            db.assert_called_once()
