import os
from datetime import date, datetime, timedelta

from django.core.mail import mail_admins

import azure
from azure.storage.blob import BlockBlobService, BlobPermissions, PublicAccess

from .models import FileBackup, FileBackupError
from . import settings as backup_settings

class BackupService:

    def __init__(self):
        self.account_name = backup_settings.BK_AZURE_ACCOUNT_NAME
        self.account_key = backup_settings.BK_AZURE_ACCOUNT_KEY
        self.azure_container = backup_settings.BK_AZURE_CONTAINER
        self.local_paths = backup_settings.BK_LOCAL_PATHS

        self.summary = []
        self._connection = None
        self.subject = 'Backup on container {}'.format(self.azure_container)

    @property
    def connection(self):
        if self._connection is None:
            self._connection = BlockBlobService(
                account_name=self.account_name,
                account_key=self.account_key)
        return self._connection

    def validate_service(self):
        if not self.account_name or not self.account_key or \
           not self.azure_container or len(self.local_paths) == 0:
            message = 'Misconfigured environment'
            mail_admins(self.subject, message)
            raise Exception(message)

    def exists(self, name):
        try:
            self.connection.get_blob_properties(
                self.azure_container, name)
        except azure.common.AzureMissingResourceHttpError:
            return False
        else:
            return True

    def check_container(self):
        containers = self.connection.list_containers()
        containers = [x.name for x in containers]
        if not self.azure_container in containers:
            self.connection.create_container(self.azure_container)

    def email_admins(self):
        if len(self.summary) == 0:
            mail_admins(self.subject, 'No files were backed up')
        else:
            full_message = ''

            for each in self.summary:
                file = '{}'.format(each['file'])
                if each['status'] == 'error':
                    file = '{}: ERROR ({})'.format(file, each['message'])
                full_message = '{}{}\n'.format(full_message, file)

            mail_admins(self.subject, full_message)

    def upload_file(self, azure_path, file_path):
        try:
            content = open(file_path, 'rb')
            self.connection.create_blob_from_stream(
                self.azure_container, azure_path, content
            )
            self.summary.append({
                "file": file_path,
                "status": "ok",
                "message": ""
            })
            return True
        except Exception as e:
            self.summary.append({
                "file": file_path,
                "status": "error",
                "message": str(e)
            })
            return False


    def retry_files_with_errors(self):
        files = FileBackupError.objects.filter(retry=True)
        for file in files:
            if os.path.isfile(file.file_path):
                file.retries += 1
                success = self.upload_file(file.azure_path, file.file_path)
                if success:
                    file.file_backup.status = 'completed'
                    file.file_backup.save()
                    file.retry = False
                file.save()
            else:
                file.retry = False
                file.save()

    def run_process(self, check_date=True):
        self.validate_service()
        self.check_container()
        yesterday = datetime.combine(
            date.today() - timedelta(days=1),
            datetime.min.time()
        )

        for folder in self.local_paths:
            for root, dirs, files in os.walk(folder['path']):
                for each in files:
                    upload = True
                    full_path = os.path.join(root, each)
                    if check_date:
                        modified = datetime.fromtimestamp(os.path.getmtime(full_path))
                        if modified < yesterday:
                            upload = False

                    if upload:
                        log = FileBackup(file_path=full_path)
                        log.save()

                        name = full_path.replace(folder['path'], folder['name'])
                        success = self.upload_file(name, full_path)

                        if success:
                            log.status = 'completed'
                            log.save()
                        else:
                            log.status = 'error'
                            log.save()
                            FileBackupError(
                                file_path=full_path,
                                azure_path=name,
                                file_backup=log
                            ).save()

        self.retry_files_with_errors()
        self.email_admins()
