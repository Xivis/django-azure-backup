from django.db import models


class FileBackup(models.Model):

    STATUS = (
        ('initial', 'Initial'),
        ('created', 'Created'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('error', 'Error'),
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    file_path = models.CharField(max_length=255, null=False, blank=False)
    status = models.CharField(max_length=255, null=False, blank=False, choices=STATUS, default='initial')
    comment = models.TextField()

    def __str__(self):
        return '{} - {} - {}'.format(
            self.file_path, self.created_at.strftime("%Y-%m-%d %H:%M"), self.status
        )


class FileBackupError(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    file_path = models.CharField(max_length=255, null=False, blank=False)
    azure_path = models.CharField(max_length=255, null=False, blank=False)
    retry = models.BooleanField(default=True)
    retries = models.IntegerField(default=0)
    file_backup = models.ForeignKey(FileBackup, on_delete=models.SET_NULL)

    def __str__(self):
        if self.retry:
            return 'PENDING - {}'.format(self.file_path)
        return 'Done - {}'.format(self.file_path)
