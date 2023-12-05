from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django.forms import ModelForm

from .models import Post, Comment


class EditProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
        ]


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = [
            'title',
            'text',
            'image',
            'pub_date',
            'location',
            'category'
        ]


class AddCommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
