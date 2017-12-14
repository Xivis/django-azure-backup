from django.contrib import admin
from .models import FileBackup, FileBackupError


admin.site.register(FileBackup)
admin.site.register(FileBackupError)
