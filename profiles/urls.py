
from django.urls import path, include
from .views import my_profile_view,invities_recived_view

urlpatterns = [
    path("myprofile", my_profile_view,name='my_profile'),
    path("my-invities", invities_recived_view,name='my-invities-view'),
]