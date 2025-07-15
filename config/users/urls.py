from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView, ProfileView, UserPublicProfileView

urlpatterns = [
    # Auth
    path('register/', RegisterView.as_view(), name='api-register'),
    path('login/', TokenObtainPairView.as_view(), name='api-login'),
    path('token/refresh', TokenRefreshView.as_view(), name='api-token-refresh'),

    # Profile
    path('me/', ProfileView.as_view(), name='api-me'),
    path('<int:pk>/', UserPublicProfileView.as_view(), name='api-user-profile'),
]
