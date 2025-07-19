from django.urls import path
from .views import FollowUserView, FollowersListView, FollowingListView

urlpatterns = [
    path('<uuid:user_id>/follow/', FollowUserView.as_view(), name='follow-user'),
    path('<uuid:user_id>/followers/', FollowersListView.as_view(), name='followers-list'),
    path('<uuid:user_id>/following/', FollowingListView.as_view(), name='following-list'),
]
