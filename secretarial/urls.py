from django.urls import path
from secretarial.views import SecretarialHomeView

app_name = 'secretarial'

urlpatterns = [
    path('', SecretarialHomeView.as_view(), name="home"),
]
