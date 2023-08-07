from django.core.management.base import BaseCommand
from datetime import datetime, timedelta
from user_management_functionlaties.models import DateTimeRecord
import pytz


class Command(BaseCommand):
    """
    Django management command to create 100 DateTimeRecord objects with their datetime
    field set to the current time in the PST timezone. Each subsequent record's datetime
    is set to one minute after the previous record's datetime.

    This command is useful for populating the database with DateTimeRecord objects for
    testing or development purposes.
    """

    help = 'Create 100 PST date times'

    def handle(self, *args, **kwargs):
        """
        The handle method is called when the command is run. It creates 100 DateTimeRecord
        objects with their datetime set to the current time in the PST timezone and
        increments one minute for each subsequent record.
        """

        pst = pytz.timezone('America/Los_Angeles')
        date_time_records = [
            DateTimeRecord(datetime=datetime.now(pst) + timedelta(minutes=i))
            for i in range(100)
        ]
        DateTimeRecord.objects.bulk_create(date_time_records)
        self.stdout.write(self.style.SUCCESS('Successfully created 100 PST date times'))
