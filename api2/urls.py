from django.urls import path
from api2 import views

urlpatterns = [
    path("comments/<int:post_id>", views.CommentListAPIView.as_view(), name="comment-filter"),
]
