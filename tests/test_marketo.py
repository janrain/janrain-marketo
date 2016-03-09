# -*- coding: utf-8 -*-
import unittest
import unittest.mock
from janrain_marketo.lib import marketo

class MarketoTests(unittest.TestCase):

    def test_upsert_leads(self):
        client = unittest.mock.Mock()
        client.execute.side_effect = [[{} for x in range(5)] for y in range(3)]
        records = [
            (
                {"janrainUUID": "{}".format(i)}, 'last{}'.format(i)
            )
            for i in range(13)
        ]
        lookup_field = 'janrainUUID'
        batch_size = 5

        results = list(marketo.upsert_leads(client, records, lookup_field, batch_size))

        expected = [
            (
                {}, '{}'.format(x), 'last4'
            ) for x in range(5)
        ]
        expected.extend([
            (
                {}, '{}'.format(x), 'last9'
            ) for x in range(5, 10)
        ])
        expected.extend([
            (
                {}, '{}'.format(x), 'last12'
            ) for x in range(10, 13)
        ])

        self.assertEqual(results, expected)
