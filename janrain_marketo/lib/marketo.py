"""Marketo helper functions."""

def upsert_leads(client, records, lookup_field, batch_size):
    """Upsert leads into marketo.

    Args:
        client: marketo client
        records: iterator of records to upsert
        lookup_field: field to use for de-duping records
        batch_size: size limit for batches sent to marketo

    Yields:
        tuple (upsert result, record lookup field value, latest lastupdated value)
    """
    batch = []
    lastest_lastupdated = ''
    for record, lastupdated in records:
        if lastupdated > lastest_lastupdated:
            latest_lastupdated = lastupdated
        batch.append(record)
        if len(batch) == batch_size:
            response = client.execute(
                method='create_update_leads',
                leads=batch,
                lookupField=lookup_field)
            for result, record in zip(response, batch):
                yield result, record[lookup_field], latest_lastupdated
            batch = []
    if batch:
        response = client.execute(
            method='create_update_leads',
            leads=batch,
            lookupField=lookup_field)
        for result, record in zip(response, batch):
            yield result, record[lookup_field], latest_lastupdated
