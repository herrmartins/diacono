from django.db import models
from core.models import BaseModel
from users.models import CustomUser


class Event(BaseModel):
    user = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True, blank=True
    )
    title = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateTimeField(blank=False, null=False)
    end_date = models.DateTimeField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    location = models.ForeignKey("events.Venue", on_delete=models.PROTECT)
    contact_user = models.ForeignKey(
        "users.CustomUser",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="event_custom_user",
    )
    contact_name = models.CharField(max_length=100, null=True, blank=True)
