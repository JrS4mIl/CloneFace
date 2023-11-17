
from django.urls import path, include
from .views import my_profile_view,invities_recived_view,profile_list_view,invite_profiles_list_view

urlpatterns = [
    path("myprofile", my_profile_view,name='my_profile'),
    path("my-invities", invities_recived_view,name='my-invities-view'),
    path("all-profiles", profile_list_view,name='all-profiles-list'),
    path("to-invite",invite_profiles_list_view,name='invite-profiles-view'),
]
