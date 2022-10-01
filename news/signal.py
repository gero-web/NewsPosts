from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Post, SubscriptionCategory


@receiver(m2m_changed, sender=Post.categories.through)
def signal_cat_post(sender, instance: Post, action, **kwargs):
    if action == 'post_add':
        cat = instance.categories.all()
        users = SubscriptionCategory.objects.filter(category__in=cat)
        email_users = [item.user.email for item in users]
        body_message = instance.preview()
        email_host = settings.EMAIL_HOST_USER
        subject = 'Новый пост или новость!'
        print(email_users)
        send_mail(subject=subject,
                  message=body_message,
                  from_email=email_host,
                  recipient_list=email_users)

