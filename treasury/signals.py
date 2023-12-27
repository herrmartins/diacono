from django.db.models.signals import post_save
from django.dispatch import receiver
from treasury.models import (
    MonthlyReportModel,
    MonthlyTransactionByCategoryModel,
    MonthlyBalance,
)
from .utils import get_aggregate_transactions_by_category
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from datetime import timedelta


@receiver(post_save, sender=MonthlyReportModel)
def post_save_monthly_report(sender, instance, created, **kwargs):
    if created:  # Runs only when a new instance is created
        year = instance.month.year
        month = instance.month.month
        report_month = instance.month

        report_month += relativedelta(months=+1)

        positive_transactions_dict = get_aggregate_transactions_by_category(
            year, month, True
        )
        negative_transactions_dict = get_aggregate_transactions_by_category(
            year, month, False
        )

        print("TRANSAÇÕES POSITIVAS NO POST_SAVE:", positive_transactions_dict)
        print("TRANSAÇÕES NEGATIVAS NO POST_SAVE:", negative_transactions_dict)

        save_transactions(positive_transactions_dict, instance, is_positive=True)
        save_transactions(negative_transactions_dict, instance, is_positive=False)


def save_transactions(transactions_dict, instance, is_positive):
    for category, total_amount in transactions_dict.items():
        MonthlyTransactionByCategoryModel.objects.create(
            report=instance,
            category=category,
            total_amount=total_amount,
            is_positive=is_positive,
        )


@receiver(post_save, sender=MonthlyBalance)
def create_missing_monthly_balances(sender, instance, created, **kwargs):
    if created:
        # Get the month the user saved
        instance_month = instance.month

        # Get the current date
        current_date = timezone.now().date()  # Extract date only

        # Loop through from the saved month to the current month
        while instance_month.year < current_date.year or (
            instance_month.year == current_date.year
            and instance_month.month <= current_date.month
        ):
            # Check if the MonthlyBalance for the instance_month exists
            if not MonthlyBalance.objects.filter(month=instance_month).exists():
                # Create the missing MonthlyBalance
                is_first = (
                    instance_month == instance.month
                )  # Flag only for initial month
                MonthlyBalance.objects.create(
                    month=instance_month,
                    is_first_month=is_first,
                    balance=instance.balance,
                )

            # Move to the next month
            next_month = instance_month.replace(day=1) + timedelta(days=32)
            instance_month = next_month.replace(day=1)
