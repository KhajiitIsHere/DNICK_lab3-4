from django.contrib import admin
from django.db.models.expressions import RawSQL
from rangefilter.filters import DateRangeFilter

from .models import *
from django.contrib.admin import DateFieldListFilter

# Register your models here.


class BlockedUsersAdmin(admin.StackedInline):
    model = BlockedUsers
    fk_name = 'from_user'
    extra = 0


class AuthorAdmin(admin.ModelAdmin):
    inlines = (BlockedUsersAdmin,)

    def has_change_permission(self, request, obj=None):
        if obj is not None and request.user.id == obj.user.id:
            return True
        else:
            return False


admin.site.register(Author, AuthorAdmin)


class CommentAdmin(admin.ModelAdmin):

    def has_change_permission(self, request, obj=None):
        if obj is not None and (request.user.id == obj.writer.user.id or request.user.id == obj.on_blog.author.user.id):
            return True
        else:
            return False


admin.site.register(Comment, CommentAdmin)


class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'content')
    search_fields = ('title', 'content')
    list_filter = ('date_created',)

    def has_change_permission(self, request, obj=None):
        if obj is not None and request.user.id == obj.author.user.id:
            return True
        else:
            return False

    def get_queryset(self, request):
        is_blocked_user = Author.objects.filter(user_id=request.user.id).first()

        if is_blocked_user is None:
            return Blog.objects.all()

        return Blog.objects.filter(id__in=RawSQL("""
            SELECT blog.id FROM Blog_blog AS blog, Blog_author AS author, Blog_blockedusers AS blocked
            WHERE blog.author_id=author.id AND author.id=blocked.from_user_id AND blocked.blocked_user_id<>%s
        """, [is_blocked_user.id])).all()


admin.site.register(Blog, BlogAdmin)