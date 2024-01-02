from django.db.models.signals import pre_save
from django.dispatch import receiver
from treasury.models import TransactionModel
from django.db.models import Sum
from decimal import Decimal


@receiver(pre_save, sender=TransactionModel)
def update_monthly_balance_on_edit(sender, instance, **kwargs):
    if instance.pk:  # Only proceed if it's an existing instance being edited
        old_instance = TransactionModel.objects.get(pk=instance.pk)
        old_amount = Decimal(old_instance.amount)
        new_amount = Decimal(instance.amount)

        if old_amount != new_amount:
            month = instance.date.replace(day=1)
            difference = new_amount - old_amount

            from treasury.models import MonthlyBalance
            from dateutil.relativedelta import relativedelta

            try:
                monthly_balance = MonthlyBalance.objects.get(month=month)
                monthly_balance.balance += difference
                monthly_balance.save()
            except MonthlyBalance.DoesNotExist:
                pass  # Handle the case if MonthlyBalance doesn't exist for the month

            # Update subsequent months' balances
            subsequent_months = MonthlyBalance.objects.filter(month__gt=month)

            for sub_month in subsequent_months:
                previous_sub_month = sub_month.month - relativedelta(months=1)
                try:
                    previous_month_balance = MonthlyBalance.objects.get(
                        month=previous_sub_month
                    )
                    prev_balance = previous_month_balance.balance
                except MonthlyBalance.DoesNotExist:
                    prev_balance = 0

                sub_month_transactions = TransactionModel.objects.filter(
                    date__year=sub_month.month.year,
                    date__month=sub_month.month.month,
                )

                sub_month_total_amount = (
                    sub_month_transactions.aggregate(total_amount=Sum("amount"))[
                        "total_amount"
                    ]
                    or 0
                )

                prev_balance += sub_month_total_amount
                sub_month.balance = prev_balance
                sub_month.save()
