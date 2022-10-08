from celery import Celery
from celery.schedules import crontab
from os import environ

environ.setdefault('DJANGO_SETTINGS_MODULE', 'news_portal.settings')

app = Celery('news_portal')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.beat_schedule = {
    'spam_monday_8h': {
        'task': 'news.tasks.spam_news',
        'schedule': crontab(hour=8, minute=0, day_of_week=1),
    }
}
app.autodiscover_tasks()
