from __future__ import absolute_import, unicode_literals
import os

from celery import Celery
from celery.schedules import crontab
from django.conf import settings

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bulk_users_mail_proj.settings')

app = Celery('bulk_users_mail_proj')
# default-ly django use utc but we want it to use asia/kolkata timezone so we make this false
app.conf.enable_utc = False
app.conf.update(timezone='Asia/Kolkata')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# CELERY BEAT SETTINGS
app.conf.beat_schedule = {
    # 'send_mail_at_7pm': {
    #     'task': 'send_mail_app.tasks.mailing_func',
    #     'schedule': crontab(hour=18, minute=18),
    #     # 'args': (2)
    # }
}

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')



