# Django Azure Cloud Backup

Library to configure backups in Azure Blob Storage of files within the project.

## Instalation

```
pip install -e git+https://github.com/ragonzal/django-azure-backup.git@master#egg=django_azure_backup
```

Or if you want to add it to your requirements.txt
```
-e git+https://github.com/ragonzal/django-azure-backup.git@master#egg=django_azure_backup
```


In your settings.py, add the package to your installed apps:
```
INSTALLED_APPS = (
    ...,
    'django_azure_backup',
)
```

Configure in you `local_settings` the following variables:

```
BK_AZURE_ACCOUNT_NAME = '...'
BK_AZURE_ACCOUNT_KEY = '...'
BK_AZURE_CONTAINER = '...'
BK_LOCAL_PATHS = [
    {"name": "backups", "path": "/path/to/folder"},
]
```


### Management command

Execute `python manage.py azure_backup_process` in a daily basis, to upload files that were modified after yesterday at 00:00