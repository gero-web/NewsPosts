from django.forms import ModelForm,DecimalField, HiddenInput
from .models import Post


class NewsAndPostForms(ModelForm):
    rating = DecimalField(widget=HiddenInput(), initial=0.0)

    class Meta:
        model = Post
        fields = [
            'author',
            'title',
            'categories',
            'body',
        ]
