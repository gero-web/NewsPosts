from celery import shared_task
from .models import SubscriptionCategory, Post
from django.conf import settings
from collections import defaultdict
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.timezone import now


@shared_task()
def new_news(cat, body_message):
    subject = 'Новый пост или новость!'
    email_host = settings.EMAIL_HOST_USER
    users = SubscriptionCategory.objects.filter(category_id__in=cat)
    print(cat)
    email_users = [item.user.email for item in users]
    send_mail(subject=subject,
              message=body_message,
              from_email=email_host,
              recipient_list=email_users)


@shared_task
def spam_news():
    all_subs = SubscriptionCategory.objects.all()
    message = defaultdict(set)

    year, week, _ = now().isocalendar()
    for sub in all_subs:
        posts = {f'http://127.0.0.1:8000/' + f'{post.pk}' for post in Post.objects.filter(categories=sub.category,
                                                                                          created__week=week)}
        message[sub.user.email] = message[sub.user.email].union(posts)

    for key, value in message.items():
        html = render_to_string(template_name='mail_template.html', context={'posts': value})
        send_mail('Рассылка', message='Добрый день!!', from_email=settings.EMAIL_HOST_USER, html_message=html,
                  recipient_list=[key])
