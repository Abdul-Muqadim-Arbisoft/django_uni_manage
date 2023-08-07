from django.core.management.base import BaseCommand
from user_management_functionlaties.models import DateTimeRecord
import pytz


class Command(BaseCommand):
    """
    Django management command to convert date times between PST and UTC.
    This command first tries to find any DateTimeRecord that is in PST and not yet converted to UTC.
    If such records exist, it converts the first 10 such records to UTC.
    If all DateTimeRecord have been converted to UTC, then it finds any DateTimeRecord that is in UTC,
    and converts the first 10 such records back to PST.
    """

    help = 'Convert 10 PST date times to UTC and vice versa'

    def handle(self, *args, **kwargs):
        """
        The handle method is called when the command is run. It first checks for any DateTimeRecord
        that is not yet converted to UTC, converts it, and saves the record back to the database.
        If all records are converted to UTC, it converts them back to PST.
        """

        utc = pytz.UTC
        pst = pytz.timezone('America/Los_Angeles')

        # Check if there are any DateTimeRecord that have not been converted to UTC
        to_convert_to_utc = DateTimeRecord.objects.filter(converted_to_utc=False)[:10]
        if to_convert_to_utc.exists():
            for record in to_convert_to_utc:
                record.datetime = record.datetime.astimezone(utc)
                record.converted_to_utc = True

            DateTimeRecord.objects.bulk_update(to_convert_to_utc, ['datetime', 'converted_to_utc'])
            self.stdout.write(self.style.SUCCESS(f'Successfully converted {to_convert_to_utc.count()}'
                                                 f' PST date times to UTC'))
        else:
            # If all DateTimeRecord have been converted to UTC, convert 10 back to PST
            to_convert_to_pst = DateTimeRecord.objects.filter(converted_to_utc=True)[:10]
            for record in to_convert_to_pst:
                record.datetime = record.datetime.astimezone(pst)
                record.converted_to_utc = False

            DateTimeRecord.objects.bulk_update(to_convert_to_pst, ['datetime', 'converted_to_utc'])
            self.stdout.write(self.style.SUCCESS(f'Successfully converted {to_convert_to_pst.count()}'
                                                 f' UTC date times back to PST'))
