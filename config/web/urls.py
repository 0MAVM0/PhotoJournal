from django.urls import path
from .views import HomeView, RegisterPageView, LoginPageView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('register/', RegisterPageView.as_view(), name='register'),
    path('login/', LoginPageView.as_view(), name='login'),
]
