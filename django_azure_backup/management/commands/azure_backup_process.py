from django.core.management.base import BaseCommand
from django_azure_backup.services import BackupService


class Command(BaseCommand):
    help = "Command to send tracked files for backup to Azure Storage"

    def add_arguments(self, parser):
        parser.add_argument('check_date', type=int, nargs='?', default=1)

    def handle(self, *args, **options):
        check_date = True if options.get('check_date', 0) == 1 else False
        service = BackupService()
        service.run_process(check_date)
