from django import forms
from .models import Post,Comment


class NewPostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']


class NewCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['massage']