from django import forms
from django.contrib.auth.models import Group
from allauth.account.forms import SignupForm

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['categories', 'title', 'content']


class BasicSignupForm(SignupForm):
    def save(self, request):
        user = super().save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user
