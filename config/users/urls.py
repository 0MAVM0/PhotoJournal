from django.urls import path
from rest_framework_simplejwt.views import ( TokenObtainPairView, TokenRefreshView )
from .views import RegisterView, ProfileView, UserPublicProfileView

urlpatterns = [
    # Auth
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),

    # Profile
    path('me/', ProfileView.as_view(), name='me'),
    path('<int:pk>/', UserPublicProfileView.as_view(), name='user-profile'),
]
