from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import Group

from allauth.account.forms import SignupForm


from .models import Post


class PostForm(forms.ModelForm):
    title = forms.CharField(
        min_length=20,
        widget=forms.Textarea({'cols': 70, 'rows': 3})
    )
    content = forms.CharField(
        min_length=200,
        widget=forms.Textarea({'cols': 70, 'rows': 20})
    )

    class Meta:
        model = Post
        fields = [
            'author',
            'category',
            'title',
            'content',
        ]

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        content = cleaned_data.get('content')
        if content == title:
            raise ValidationError(
                'Текст не должен совпадать с заголовком.'
            )

        return cleaned_data


class CommonSignupForm(SignupForm):

    def save(self, request):
        user = super(CommonSignupForm, self).save(request)
        common_group = Group.objects.get(name='common')
        common_group.user_set.add(user)
        return user
