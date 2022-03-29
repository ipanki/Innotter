from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from profiles.models import Post, Page, Comment, User

admin.site.register(User)


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    readonly_fields = ('owner', 'uuid', 'id')
    list_display = ('owner', 'id', 'uuid', 'name', 'description', 'image', 'is_private')
