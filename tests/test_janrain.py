# -*- coding: utf-8 -*-
import unittest
import unittest.mock
from janrain_marketo.lib import janrain

class JanrainTests(unittest.TestCase):

    def test_capture_records(self):
        records = unittest.mock.MagicMock()
        records.iterator.return_value = [
            {'uuid': '{}'.format(x), 'lastUpdated': 'abc'} for x in range(13)
        ]
        attribute_map = {
            'uuid': 'janrainUUID'
        }
        last_updated = 'abc'
        batch_size = 5
        results = list(janrain.capture_records(records, attribute_map, last_updated, batch_size))

        expected = [
            ({'janrainUUID': '{}'.format(x)}, 'abc') for x in range(13)
        ]

        self.assertEqual(results, expected)

        records.iterator.called_with(
            attributes=['uuid', 'lastUpdated'],
            batch_size=batch_size,
            filtering="lastUpdated > '{}'".format(last_updated))
