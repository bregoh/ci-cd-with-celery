import os
from celery import Celery
from django.conf import settings


# set the default Django settings module for the 'celery' app.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")

# you can change the name here
app = Celery("server")

# read config from Django settings, the CELERY namespace would make celery
# config keys has `CELERY` prefix
app.config_from_object("django.conf:settings", namespace="CELERY")

# discover and load tasks.py in django apps
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
