"""User models admin."""

# Django
from django.contrib import admin

# Project
from .models import Profile, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """User model admin."""
    
    list_display = ('email', 'created', 'modified')
    search_fields = ('email', 'created', 'modified')
    list_filter = ('email', 'created', 'modified')


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Profile model admin."""

    list_display = ('user', 'first_name', 'last_name', 'bio', 'birthday')
    search_fields = ('user', 'first_name', 'last_name', 'bio', 'birthday')
    list_filter = ('user', 'first_name', 'last_name', 'bio', 'birthday')
