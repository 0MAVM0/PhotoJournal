from django.urls import path
from .views import LikePostView

urlpatterns = [
    path('', LikePostView.as_view(), name='api-like-post'),
]
