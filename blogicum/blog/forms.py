from django import forms

from blog.models import Comment, Post, User


class PostCreateForm(forms.ModelForm):

    class Meta:
        model = Post
        exclude = ('author',)
        widgets = {
            'pub_date': forms.DateTimeInput(
                format='%Y-%m-%d %H:%M:%S',
                attrs={'class': 'datetimefield'}
            ),
        }


class UserEditForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email',)


class CommentForm(forms.ModelForm):
    text = forms.CharField(
        widget=forms.Textarea(attrs={'cols': 10, 'rows': 5})
    )

    class Meta:
        model = Comment
        fields = ('text',)
