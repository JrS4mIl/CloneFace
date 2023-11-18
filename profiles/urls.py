from django.urls import path, include
from .views import my_profile_view, invities_recived_view, profile_list_view, invite_profiles_list_view,remove_from_friends,ProfileListView, send_invatation,accept_invatation,reject_invatation

urlpatterns = [
    path("myprofile", my_profile_view, name='my_profile'),
    path("my-invities", invities_recived_view, name='my-invities-view'),
    path("all-profiles", ProfileListView.as_view(), name='all-profiles-list'),
    path("to-invite", invite_profiles_list_view, name='invite-profiles-view'),
    path("send-invite", send_invatation, name='send-invite'),
    path("remove-friend", remove_from_friends, name='remove-friend'),
    path("my-invities/acctep/", accept_invatation, name='accept-invite'),
    path("my-invities/reject/", remove_from_friends, name='reject-invite'),
]
