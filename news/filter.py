from django_filters import FilterSet, ModelMultipleChoiceFilter, DateFilter
from django.forms import DateInput
from .models import Post, Category


class PostFilter(FilterSet):
    categories = ModelMultipleChoiceFilter(
        field_name='categories__name_category',
        queryset=Category.objects.all(),
        label='Categories',
    )

    created = DateFilter(
        field_name='created__date',
        lookup_expr='gt',
        label='Date',
        widget=DateInput(
            attrs={
                'type': 'date'
            }
        )
    )

    class Meta:
        model = Post
        fields = {
            'title': ['icontains'],
        }
