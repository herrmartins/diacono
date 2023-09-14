from django.urls import path
from django.contrib.auth.views import LogoutView
from users.views import RegisterFormView
from users.views import UserProfileView, UserProfileUpdateView

app_name = 'users'

urlpatterns = [
    path('register', RegisterFormView.as_view(), name="register"),
    path('logout', LogoutView.as_view(), name="logout"),
    path('profile/<int:pk>', UserProfileView.as_view(), name="user-profile"),
    path('profile/update/<int:pk>',
         UserProfileUpdateView.as_view(), name="user-profile-update"),
]
