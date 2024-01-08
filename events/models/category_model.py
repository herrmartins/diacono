from django.db import models
from core.models import BaseModel


class EventCategory(BaseModel):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name
