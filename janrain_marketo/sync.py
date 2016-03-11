"""Sync endpoint"""
import flask
import logging
import pynamodb.exceptions
import time
from janrain_marketo.lib import db
from janrain_marketo.lib import janrain
from janrain_marketo.lib import marketo

def start_sync():
    """Initiate sync between Janrain and Marketo."""
    config = flask.current_app.config
    janrain_records = flask.current_app.janrain_records
    marketo_client = flask.current_app.marketo_client

    logger = logging.getLogger(config['LOGGER_NAME'])

    try:
        job = db.JobsModel.get(config['JANRAIN_URI'])
    except pynamodb.exceptions.DoesNotExist:
        job = db.JobsModel(config['JANRAIN_URI'])

    if job.start(config['DB_UPDATE_INTERVAL']):

        if job.lastupdated:
            logger.info("syncing janrain records updated since {}".format(job.lastupdated))
        else:
            logger.info('syncing all janrain records')

        janrain_records_iter = janrain.capture_records(
            janrain_records,
            config['JANRAIN_MARKETO_FIELD_MAP'],
            job.lastupdated,
            config['JANRAIN_BATCH_SIZE_LIMIT'],
        )

        lookup_field = config['JANRAIN_MARKETO_FIELD_MAP']['uuid']
        marketo_results = marketo.upsert_leads(
            marketo_client,
            janrain_records_iter,
            lookup_field,
            config['MARKETO_BATCH_SIZE_LIMIT'],
        )

        flask.current_app.executor.submit(
            do_sync,
            job,
            logger,
            marketo_results,
            config['DB_UPDATE_INTERVAL'],
            config['DEBUG'],
        )

    else:
        logger.warning("unable to start: previous job still running")

    return 'ok'

def do_sync(job, logger, marketo_results, update_interval, debug=False):
    """Sync Janrain with Marketo."""
    logger.info("start")

    last_timestamp = time.time()
    try:
        record_num = 0
        for record_num, (result, uuid, lastupdated) in enumerate(marketo_results, start=1):
            if 'id' in result:
                msg = "id {id} {status} (janrain uuid: {uuid})".format(
                    id=result['id'],
                    status=result['status'],
                    uuid=uuid)
                logger.info(msg)
            else:
                msg = "upsert failed: {reason} (janrain uuid: {uuid})".format(
                    reason=result['reasons'][0]['message'],
                    uuid=uuid)
                logger.warning(msg)
            job.lastupdated = lastupdated
            job.lastrecord = record_num
            current_timestamp = time.time()
            # update db every so often
            if last_timestamp + update_interval >= current_timestamp:
                job.save()
                last_timestamp = current_timestamp
        logger.info("synced {} records".format(record_num))

    except Exception as ex:
        job.error = str(ex)
        if debug:
            logger.exception(ex)
        else:
            logger.error(job.error)

    finally:
        job.stop()

    logger.info("end")
