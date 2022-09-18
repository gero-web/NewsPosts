from django.forms import ModelForm,DecimalField, HiddenInput, TextInput,\
    Textarea,Select
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
        widgets ={
            'author': TextInput(attrs={
                'class': 'form-control',
                'style': 'max-width: 300px;',
                }
            ),
            'title': TextInput(attrs={
                'class': 'form-control',
                'style': 'max-width: 300px;',
                 }
            ),
            'body': Textarea(attrs={
                'class': 'form-control',
                'style': 'max-width: 300px;',
             }
            ),
            'categories': Select(attrs={
                'class': 'form-select',
                'style': 'max-width: 300px;',
                }
            )
        }
