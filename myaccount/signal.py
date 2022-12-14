from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import User, Group


@receiver(post_save, sender=User)
def user_in_role(sender, instance: User, created, **kwargs):
    if created:
        group = Group.objects.get(pk=1)
        print(group)
        instance.groups.add(group)
        instance.save()
        send_mail(subject='Привет',
                  message='Добро пожаловать!',
                  from_email=settings.EMAIL_HOST_USER,
                  recipient_list=instance.email)

