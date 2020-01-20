"""
Setting up celery instance / application
"""
from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings

#setting Django settings for celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'notifications.settings')
app = Celery('notifications')

# setting up conifguration module with config details
app.config_from_object('django.conf:settings')

# search for tasks.py file from installed apps.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

#first argument to the task is the task instance (self)
@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
