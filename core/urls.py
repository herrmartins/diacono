from django.urls import path
from .views import IndexView, ConfigView

app_name = 'core'

urlpatterns = [
    path('', IndexView.as_view(), name="home"),
    path("config", ConfigView.as_view(), name="config"),
]
