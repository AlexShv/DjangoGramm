from django.urls import path
from django.views.generic import RedirectView
from .views import *


# Налаштував маршрути
urlpatterns = [
    path('register/', register, name='register'),
    path('login/', sign_in, name='login_page'),
    path('logout/', sign_out, name='logout_page'),
    path('activate/<uidb64>/<token>', activate, name='activate'),
    path('', MainPage.as_view(), name='home'),
    path('profile/<str:username>/', Profile.as_view(), name='profile'),
    path('profile/<str:username>/edit', EditProfile.as_view(), name='edit_profile'),
    path('post/<int:post_id>/', ShowPost.as_view(), name='post_detail'),
    path('post/create', add_post, name='create_post'),
    path('post/edit/<int:post_id>/', edit_post, name='post-edit'),
    path('post/delete/<int:pk>', DeletePost.as_view(), name='post_delete'),
    path('post/<int:post_id>/add_comment', add_comment, name='add_comment'),
    path('reaction/<int:post_id>', react_post, name='react_post'),
    path('follow_or_unfollow/<int:user_id>', follow_or_unfollow, name='follow_or_unfollow'),
    path('accounts/profile/', RedirectView.as_view(url='/', permanent=False), name='redirect_to_home'),
]
