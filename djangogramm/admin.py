from django.contrib import admin
from .models import *


# Реєструю моделі
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'bio')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'user_id', 'created_at', 'updated_at')


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('post', 'image',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('description', 'author', 'created_at', 'post_id')


@admin.register(Reaction)
class ReactionAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'post_id', 'type_of_reaction')


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('follower', 'followed', 'created_at')
