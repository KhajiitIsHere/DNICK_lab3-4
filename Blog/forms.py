from django import forms
from .models import Blog, BlockedUsers


class BlogForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(BlogForm, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            print(field)
            field.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = Blog
        exclude = ('author', 'date_created', 'last_changed')


class BlockedUsersForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(BlockedUsersForm, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            print(field)
            field.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = BlockedUsers
        exclude = ('from_user',)
