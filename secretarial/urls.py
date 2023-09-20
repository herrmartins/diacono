from django.urls import path
from secretarial.views import SecretarialHomeView, MinutesEditorView

app_name = 'secretarial'

urlpatterns = [
    path('', SecretarialHomeView.as_view(), name="home"),
    path('minute', MinutesEditorView.as_view(), name="minutes-editor")
]
