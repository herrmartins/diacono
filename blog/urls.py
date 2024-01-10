from django.urls import path
from blog.views import (BlogHomeView, PostFormView,
                        PostCreateView, CategoryFormView, CategoryCreateView)

app_name = "blog"

urlpatterns = [
    path("", BlogHomeView.as_view(), name="home"),
    path("create", PostCreateView.as_view(), name="create"),
    path("edit/<int:pk>", PostFormView.as_view(), name="edit"),
    path("create/category", CategoryCreateView.as_view(), name="create-category"),
    path("edit/category/<int:pk>", CategoryFormView.as_view(), name="edit-category"),
]
