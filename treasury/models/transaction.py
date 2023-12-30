from django.db import models
from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from core.models import BaseModel
from treasury.models import CategoryModel
from django.db.models import Sum
from decimal import Decimal


class TransactionModel(BaseModel):
    user = models.ForeignKey("users.CustomUser", on_delete=models.CASCADE)
    category = models.ForeignKey(
        CategoryModel, on_delete=models.SET_NULL, null=True, blank=True
    )
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_positive = models.BooleanField(default=True)
    date = models.DateField()

    edit_history = models.ManyToManyField("treasury.TransactionEditHistory", blank=True)

    class Meta:
        verbose_name = "Transação"
        verbose_name_plural = "Transações"

    def __str__(self):
        return f"{self.date} - {self.description} - R$ {self.amount}"


@receiver(post_save, sender=TransactionModel)
def update_monthly_balance(sender, instance, created, **kwargs):
    if created:
        month = instance.date.replace(day=1)
        amount = instance.amount

        from treasury.models import MonthlyBalance

        # Get or create the MonthlyBalance for the current month
        monthly_balance, _ = MonthlyBalance.objects.get_or_create(
            month=month,
            defaults={"balance": 0},
        )
        monthly_balance.balance += amount
        monthly_balance.save()

        # Get all subsequent months' balances and adjust them
        subsequent_months = MonthlyBalance.objects.filter(month__gt=month)
        prev_balance = monthly_balance.balance

        for sub_month in subsequent_months:
            sub_month_balance = (
                TransactionModel.objects.filter(
                    date__year=sub_month.month.year,
                    date__month=sub_month.month.month,
                ).aggregate(total_amount=Sum("amount"))["total_amount"]
                or 0
            )

            sub_month.balance = sub_month_balance + prev_balance
            sub_month.save()
            prev_balance = sub_month.balance


@receiver(pre_save, sender=TransactionModel)
def update_monthly_balance_on_edit(sender, instance, **kwargs):
    if instance.pk:  # If the instance has a primary key (i.e., it's an existing instance being edited)
        old_instance = TransactionModel.objects.get(pk=instance.pk)
        old_amount = old_instance.amount
        new_amount = Decimal(instance.amount)

        # Check if the amount has changed
        if old_amount != new_amount:
            # Logic to update monthly balances
            month = instance.date.replace(day=1)
            difference = new_amount - old_amount

            from treasury.models import MonthlyBalance

            monthly_balance, _ = MonthlyBalance.objects.get_or_create(
                month=month,
                defaults={"balance": 0},
            )
            monthly_balance.balance += difference
            monthly_balance.save()

            # Update subsequent months' balances
            subsequent_months = MonthlyBalance.objects.filter(month__gt=month)
            prev_balance = monthly_balance.balance

            for sub_month in subsequent_months:
                sub_month_balance = (
                    TransactionModel.objects.filter(
                        date__year=sub_month.month.year,
                        date__month=sub_month.month.month,
                    ).aggregate(total_amount=Sum("amount"))["total_amount"]
                    or 0
                )

                sub_month.balance = sub_month_balance + prev_balance
                sub_month.save()
                prev_balance = sub_month.balance


@receiver(pre_save, sender=TransactionModel)
def check_is_positive(sender, instance, **kwargs):
    if instance.amount < 0:
        instance.is_positive = False
    else:
        instance.is_positive = True


@receiver(post_delete, sender=TransactionModel)
def update_monthly_balance_on_delete(sender, instance, **kwargs):
    month = instance.date.replace(day=1)
    amount = instance.amount

    from treasury.models import MonthlyBalance

    try:
        monthly_balance = MonthlyBalance.objects.get(month=month)
        monthly_balance.balance -= amount
        monthly_balance.save()

        # Get all subsequent months' balances and adjust them
        subsequent_months = MonthlyBalance.objects.filter(month__gt=month)
        prev_balance = monthly_balance.balance

        for sub_month in subsequent_months:
            sub_month_balance = (
                TransactionModel.objects.filter(
                    date__year=sub_month.month.year,
                    date__month=sub_month.month.month,
                ).aggregate(total_amount=Sum("amount"))["total_amount"]
                or 0
            )

            sub_month.balance = sub_month_balance + prev_balance
            sub_month.save()
            prev_balance = sub_month.balance

    except MonthlyBalance.DoesNotExist:
        print("MonthlyBalance does not exist for this month")
