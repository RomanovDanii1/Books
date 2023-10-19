# books/celery.py
from __future__ import absolute_import, unicode_literals
import os
from datetime import timedelta
from . import settings

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'books.settings')
app = Celery('books')

# Load task modules from all registered Django app configs.
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


app.conf.beat_schedule = {
    'update-reading-statistics-task': {
        'task': 'api.tasks.update_reading_statistics',
        'schedule': timedelta(seconds=10),
    },
}