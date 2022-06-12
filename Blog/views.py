from django.db.models.expressions import RawSQL
from django.shortcuts import render, redirect
from .models import *
from .forms import BlogForm, BlockedUsersForm
import datetime


# Create your views here.


def posts(request):
    user = Author.objects.filter(user_id=request.user.id).first()
    blogs = Blog.objects.exclude(author_id__in=RawSQL("""
        SELECT blocked.blocked_user_id FROM Blog_blockedusers AS blocked
        WHERE blocked.from_user_id=%s
    """, [user.id])).exclude(author_id__in=RawSQL("""
        SELECT blocked.from_user_id FROM Blog_blockedusers AS blocked
        WHERE blocked.blocked_user_id=%s
    """, [user.id])).exclude(author_id=user.id)
    context = {
        'blogs': blogs
    }
    return render(request, 'posts.html', context)


def add_post(request):
    author = Author.objects.filter(user_id=request.user.id).first()
    if request.method == 'POST':
        tmp = BlogForm(request.POST)
        if tmp.is_valid():
            blog = tmp.save(commit=False)
            blog.author = author
            blog.date_created = datetime.date.today()
            blog.last_changed = datetime.date.today()
            blog.save()
        return redirect('/add/post/')
    context = {'form': BlogForm}
    return render(request, 'addPost.html', context)


def show_profile(request):
    author = Author.objects.filter(user_id=request.user.id).first()
    blogs = Blog.objects.filter(author_id=author.id)
    context = {'author': author, 'blogs': blogs}
    return render(request, 'profile.html', context)


def blocked_users(request):
    author = Author.objects.filter(user_id=request.user.id).first()

    if request.method == 'POST':
        form = BlockedUsersForm(request.POST)
        if form.is_valid():
            blocked_user = form.save(commit=False)
            blocked_user.from_user = author
            blocked_user.save()
        return redirect('/blockedUsers/')

    blocked = BlockedUsers.objects.filter(from_user_id=author.id).all()
    context = {"blocked_users": blocked, 'form': BlockedUsersForm}
    return render(request, 'blocked.html', context)
