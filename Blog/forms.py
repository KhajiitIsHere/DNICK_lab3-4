from django import forms
from .models import Blog, BlockedUsers


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        exclude = ('author', 'date_created', 'last_changed')


class BlockedUsersForm(forms.ModelForm):
    class Meta:
        model = BlockedUsers
        exclude = ('from_user',)
