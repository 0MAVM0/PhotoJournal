from django.urls import path
from .views import CommentListCreateView, CommentUpdateDeleteView

urlpatterns = [
    path('', CommentListCreateView.as_view(), name='comment-list-create'),
    path('<int:pk>/', CommentUpdateDeleteView.as_view(), name='comment-update-delete'),
]
