from django.db.models.signals import pre_save
from django.dispatch import receiver
from treasury.models.monthly_balance import MonthlyBalance
from treasury.models import TransactionModel
from treasury.utils import (
    monthly_balance_exists,
    check_and_create_missing_balances,
)
from datetime import datetime
from django.db import transaction


@receiver(pre_save, sender=TransactionModel)
def update_monthly_balance_on_create(sender, instance, **kwargs):
    if not instance.pk:
        current_month = datetime.now().replace(day=1)
        transaction_month = instance.date.replace(day=1)

        if monthly_balance_exists(transaction_month):
            with transaction.atomic():
                monthly_balance = MonthlyBalance.objects.get(month=transaction_month)
                monthly_balance.balance += instance.amount
                monthly_balance.save()

        else:
            check_and_create_missing_balances(transaction_month)
            with transaction.atomic():
                monthly_balance = MonthlyBalance.objects.get(month=transaction_month)
                monthly_balance.balance += instance.amount
                monthly_balance.save()