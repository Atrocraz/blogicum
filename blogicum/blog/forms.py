from django import forms

from blog.models import Post, Comment, User


class PostCreateForm(forms.ModelForm):

    class Meta:
        model = Post
        exclude = ('author', 'created_at', 'id')


class UserEditForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email',)


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)
