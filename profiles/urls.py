
from django.urls import path, include
from .views import my_profile_view

urlpatterns = [
    path("myprofile", my_profile_view,name='my_profile'),
]