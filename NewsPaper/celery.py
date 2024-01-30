import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPaper.settings')

app = Celery('NewsPaper')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'mailing_on_mondays_8am': {
        'task': 'News.tasks.send_weekly_mail',
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
        # 'schedule': crontab(hour=19, minute=12, day_of_week='tuesday'),
        'args': ()
    },
}

app.conf.timezone = 'UTC'
