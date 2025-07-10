from django.urls import path
from .views import CommentListCreateView, CommentUpdateDeleteView

urlpatterns = [
    path('', CommentListCreateView.as_view(), name='comment-list-create-api'),
    path('<int:pk>/', CommentUpdateDeleteView.as_view(), name='comment-update-delete-api'),
]
