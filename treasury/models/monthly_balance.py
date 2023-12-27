from core.models import BaseModel
from django.db import models


class MonthlyBalance(BaseModel):
    month = models.DateField(unique=True)
    is_first_month = models.BooleanField(default=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    class Meta:
        verbose_name = "Saldo Mensal"
        verbose_name_plural = "Saldos Mensais"

    def __str__(self):
        return f"{self.month} - {self.balance} - {self.is_first_month}"
