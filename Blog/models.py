from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Author(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profilePics/', null=True, blank=True)
    # blocked_users = models.ManyToManyField(to='self', null=True, blank=True)

    def __str__(self):
        return self.name


class BlockedUsers(models.Model):
    from_user = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='from_user')
    blocked_user = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='blocked_user')


class Blog(models.Model):
    title = models.CharField(max_length=50)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(upload_to='blogPics/', null=True, blank=True)
    date_created = models.DateField()
    last_changed = models.DateField()

    def __str__(self):
        return self.title


class Comment(models.Model):
    content = models.TextField()
    writer = models.ForeignKey(Author, on_delete=models.CASCADE)
    on_blog = models.ForeignKey(Blog, on_delete=models.CASCADE)

    def __str__(self):
        return self.content
