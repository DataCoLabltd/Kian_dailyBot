from __future__ import absolute_import, unicode_literals
from celery.schedules import crontab
import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "daily_bot.settings")
app = Celery("daily_bot")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
app.conf.timezone = 'Asia/Tehran'
app.conf.beat_schedule = {
    'alarm-to-all-users': {
        'task': 'slack_app.tasks.alarm_to_all_users',
        'schedule': crontab(hour=8, minute=30)
    },
    'add': {
        'task': 'slack_app.tasks.add',
        'schedule': crontab(hour=15, minute=0)
    }
}
