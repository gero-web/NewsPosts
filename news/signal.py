from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Post
from .tasks import new_news

@receiver(m2m_changed, sender=Post.categories.through)
def signal_cat_post(sender, instance, action, **kwargs):
    if action == 'post_add':
        cat = list(val for pk in instance.categories.all().values('pk') for _, val in pk.items())
        body_message = instance.preview()
        new_news.delay(cat, body_message)
