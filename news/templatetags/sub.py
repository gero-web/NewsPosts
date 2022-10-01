from django import template
from ..models import SubscriptionCategory

register = template.Library()


@register.filter
def has_sub(user, pk):
    return SubscriptionCategory.objects.filter(category__pk=pk, user=user).exists()
