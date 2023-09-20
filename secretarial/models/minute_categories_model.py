from django.db import models
from core.models import BaseModel


class MinuteCategoriesModel(BaseModel):
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.category
