from crispy_forms.helper import FormHelper
from django import forms

from blog.models import BlogPost


class BlogPostForm(forms.ModelForm):
    preview = forms.ImageField(label='Загрузить изображение')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'

    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'preview']
