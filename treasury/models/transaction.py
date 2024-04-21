from django.db import models
from core.models import BaseModel
from treasury.models import CategoryModel
from django.utils import timezone
from django.core.exceptions import ValidationError
from django_resized import ResizedImageField
from treasury.utils import custom_upload_to


class TransactionModel(BaseModel):
    user = models.ForeignKey("users.CustomUser", on_delete=models.CASCADE)
    category = models.ForeignKey(
        CategoryModel, on_delete=models.SET_NULL, null=True, blank=True
    )
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_positive = models.BooleanField(default=True)
    date = models.DateField()

    edit_history = models.ManyToManyField(
        "treasury.TransactionEditHistory", blank=True)

    acquittance_doc = ResizedImageField(
        size=[1200, 850], upload_to=custom_upload_to, blank=True, null=True, force_format="JPEG")

    class Meta:
        verbose_name = "Transação"
        verbose_name_plural = "Transações"

    def __str__(self):
        return f"{self.date} - {self.description} - R$ {self.amount}"

    def save(self, *args, **kwargs):
        if self.pk:
            old_record = TransactionModel.objects.get(pk=self.pk)
            if old_record.acquittance_doc != self.acquittance_doc:
                old_record.acquittance_doc.delete(save=False)

        today = timezone.now().date()
        if self.date > today:
            raise ValidationError("Cannot add transactions with a future date")

        from treasury.models import MonthlyBalance
        try:
            MonthlyBalance.objects.get(is_first_month=True)
        except MonthlyBalance.DoesNotExist:
            raise ValidationError(
                "Cannot add transactions without adding the monthly balances...")

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.acquittance_doc:
            self.acquittance_doc.delete(save=False)
        super().delete(*args, **kwargs)
