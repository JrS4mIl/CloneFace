
from django.urls import path, include
from .views import post_comment_create_and_list_view,like_unlike_post

urlpatterns = [
    path("", post_comment_create_and_list_view,name='main-post-view'),
    path("liked/", like_unlike_post,name='like-post-view'),
]