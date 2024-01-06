from treasury.models import MonthlyBalance


def monthly_balance_exists(month):
    try:
        monthly_balance = MonthlyBalance.objects.get(month=month)
        return True
    except MonthlyBalance.DoesNotExist:
        return False
