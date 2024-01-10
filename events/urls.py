from django.urls import path
from events.views import EventsHomeView, EventsFormView, EventCreateView

app_name = "events"

urlpatterns = [
    path("", EventsHomeView.as_view(), name="home"),
    path("register", EventsFormView.as_view(), name="register"),
    path("edit/<int:pk>", EventsFormView.as_view(), name="edit-event"),
    path("create", EventCreateView.as_view(), name="create-event"),
]
