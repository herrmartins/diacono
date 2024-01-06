from django.test import TestCase
from model_mommy import mommy
from treasury.models.transaction import TransactionModel
from treasury.models import MonthlyBalance
from django.utils import timezone
from dateutil.relativedelta import relativedelta


class MonthlyBalanceModelTest(TestCase):
    def setUp(self):
        self.current_month = timezone.now().date().replace(day=1)
        self.a_year_ago = self.current_month - relativedelta(months=12)
        self.balance = MonthlyBalance.objects.create(
            month=self.a_year_ago, is_first_month=True, balance=0
        )

    def test_monthly_balance_creation(self):
        print("MESES CRIADOS:", MonthlyBalance.objects.all())
        self.assertTrue(isinstance(self.balance, MonthlyBalance))
        self.assertEqual(
            self.balance.__str__(),
            f"{self.balance.month} - {self.balance.balance} - {self.balance.is_first_month}",
        )

    def test_unique_month(self):
        with self.assertRaises(Exception):
            duplicate_balance = MonthlyBalance.objects.create(
                month=self.current_month, is_first_month=True, balance=200.0
            )

    def test_delete_balance(self):
        with self.assertRaises(Exception):
            MonthlyBalance.objects.get(month=self.current_month).delete()

    def test_create_transaction_without_any_balances(self):
        MonthlyBalance.objects.all().delete()
        with self.assertRaises(Exception):
            mommy.make(TransactionModel)
