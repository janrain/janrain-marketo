import time
import pynamodb.attributes
import pynamodb.exceptions
import pynamodb.models
from janrain_marketo.config import get_config

config = get_config()

class JobsModel(pynamodb.models.Model):
    """DyanmoDB table structure."""

    class Meta:
        region = config['AWS_DEFAULT_REGION']
        table_name = config['AWS_DYNAMODB_TABLE']
        host = config['AWS_DYNAMODB_URL']

    job_id = pynamodb.attributes.UnicodeAttribute(hash_key=True)
    job_updated = pynamodb.attributes.NumberAttribute(null=True)
    lastrecord = pynamodb.attributes.NumberAttribute(null=True)
    started = pynamodb.attributes.NumberAttribute(null=True)
    ended = pynamodb.attributes.NumberAttribute(null=True)
    lastupdated = pynamodb.attributes.UnicodeAttribute(null=True)
    error = pynamodb.attributes.UnicodeAttribute(null=True)

    def start(self, update_interval):
        """Start the job. Can only be started if stalled or completed.

        Args:
            update_interval: seconds between updates

        Returns:
            bool (whether start succeeded)
        """
        self.lastrecord = 0
        self.started = time.time()
        self.ended = None
        self.error = None

        if self.job_updated:
            # job is stalled
            if self.started > self.job_updated + update_interval * 2:
                # force it to start again
                self.job_updated = self.started
                self.save()
            else:
                # job is running
                return False
        else:
            self.job_updated = self.started
            try:
                self.save(job_updated__null=True)
            except pynamodb.exceptions.PutError as ex:
                if 'ConditionalCheckFailedException' in str(ex):
                    # job is running
                    return False
                raise
        return True

    def stop(self):
        """Stop the job."""
        self.ended = time.time()
        self.job_updated = None
        self.save()
