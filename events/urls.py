from django.urls import path
from events.views import EventsHomeView

app_name = "events"

urlpatterns = [
    path("", EventsHomeView.as_view(), name="home"),
]
