from django.urls import path
from .views import FollowUserView, FollowersListView, FollowingListView

urlpatterns = [
    path('<str:username>/follow/', FollowUserView.as_view(), name='follow-user'),
    path('<str:username>/followers/', FollowersListView.as_view(), name='followers-list'),
    path('<str:username>/following/', FollowingListView.as_view(), name='following-list'),
]
