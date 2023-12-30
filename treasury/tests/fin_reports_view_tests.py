from django.test import TestCase
from django.urls import reverse
from users.models import CustomUser
from treasury.models import MonthlyBalance
from django.test.client import Client
from datetime import datetime, date
from django.contrib.auth.models import Group, Permission
from treasury.models import TransactionModel
from model_mommy import mommy


class FinanceReportsListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = CustomUser.objects.create_user(
            username="testuser", email="test@example.com", password="password123"
        )
        cls.treasury_group = Group.objects.create(name="treasury")
        cls.permission = Permission.objects.get(codename="view_transactionmodel")
        cls.treasury_group.permissions.add(cls.permission)
        cls.user.groups.add(cls.treasury_group)

        cls.monthly_balance_2 = mommy.make(
            "treasury.MonthlyBalance",
            month=datetime.strptime("2023-02-01", "%Y-%m-%d").date(),
        )

    def setUp(self):
        self.client = Client()
        self.user.user_permissions.add(self.permission)
        self.client.login(username="testuser", password="password123")

    def test_user_has_required_permission(self):
        response = self.client.get(reverse("treasury:list-financial-reports"))
        self.assertEqual(response.status_code, 200)

        self.assertTrue(
            self.user.has_perm("treasury.view_transactionmodel"),
            msg="User doesn't have the required permission.",
        )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get("/treasury/reports")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse("treasury:list-financial-reports"))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse("treasury:list-financial-reports"))
        self.assertTemplateUsed(response, "treasury/reports_list.html")

    def test_view_context_contains_reports(self):
        response = self.client.get(reverse("treasury:list-financial-reports"))
        reports_context = response.context.get("reports")

        self.assertIsNotNone(reports_context, msg="Reports context is None")

        self.assertTrue(
            all(isinstance(report, MonthlyBalance) for report in reports_context),
            msg="Reports context contains non-MonthlyBalance objects",
        )

        self.assertGreaterEqual(
            len(reports_context),
            1,
            msg="Reports context does not contain any MonthlyBalance instance",
        )

    def test_monthly_balance_str_representation(self):
        monthly_balance = MonthlyBalance.objects.create(
            month=date(2023, 1, 1), is_first_month=True, balance=1000.00
        )
        monthly_balance = MonthlyBalance.objects.get(month="2023-01-01")
        self.assertEqual(str(monthly_balance), "2023-01-01 - 1000.00 - True")
