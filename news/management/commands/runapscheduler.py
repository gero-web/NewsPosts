# runapscheduler.py
import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from news.models import Category, SubscriptionCategory, Post
from collections import defaultdict
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.sites.models import Site
from django.utils.timezone import now

logger = logging.getLogger(__name__)


def my_job():
    all_subs = SubscriptionCategory.objects.all()
    message = defaultdict(set)
    #я не знаю как можно сделать еще рассылку
    # подскажите если не сложно

    year, week, _ = now().isocalendar()
    current_site = Site.objects.get_current()
    for sub in all_subs:
        posts = { f'http://127.0.0.1:8000/' + f'{post.pk}' for post in Post.objects.filter(categories=sub.category,
                                                                                                created__week=week)}
        message[sub.user.email] = message[sub.user.email].union(posts)

    for key, value in message.items():
        html = render_to_string(template_name='mail_template.html', context={'posts': value})
        send_mail('Рассылка', message='Добрый день!!', from_email=settings.EMAIL_HOST_USER, html_message=html,
                  recipient_list=[key])
    print(message)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            my_job,
            trigger=CronTrigger(day_of_week='*/6'),  # Every 7 day
            id="my_job",  # The `id` assigned to each job MUST be unique
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
