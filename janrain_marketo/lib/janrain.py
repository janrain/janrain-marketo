"""Janrain helper functions."""
import janrain_datalib.utils

def capture_records(records, attribute_map, last_updated, batch_size):
    attributes = list(attribute_map.keys())
    if 'lastUpdated' not in attributes:
        attributes.append('lastUpdated')
    kwargs = {
        'attributes': attributes,
        'batch_size': batch_size,
    }
    if last_updated:
        kwargs['filtering'] = "lastUpdated > '{}'".format(last_updated)

    for record in records.iterator(**kwargs):
        # flatten and rename keys
        new_record = {}
        for janrain_attribute in attribute_map:
            key = attribute_map[janrain_attribute]
            value = janrain_datalib.utils.dot_lookup(record, janrain_attribute)
            new_record[key] = value

        yield new_record, record['lastUpdated']
