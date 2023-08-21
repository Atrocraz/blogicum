# birthday/forms.py
from django import forms
from django.contrib.auth import get_user_model
from .models import Post
from django.contrib.auth.forms import UserChangeForm

User = get_user_model()


class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ('author',)


class UserEditForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('password')


class PostEditForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ('id', 'created_at', 'author_id', )
