from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.utils import timezone
from treasury.models import MonthlyBalance, TransactionModel
from secretarial.models import (
    MinuteExcerptsModel,
    MeetingMinuteModel,
    MinuteTemplateModel,
)
from users.models import CustomUser
from secretarial.models import (
    MinuteExcerptsModel,
    MeetingMinuteModel,
    MinuteTemplateModel,
)
from decimal import Decimal
from model_mommy import mommy
from datetime import datetime, date


class TestViews(APITestCase):
    def setUp(self):
        self.date = date(2023, 12, 1)
        self.date_before = date(2023, 11, 1)
        self.user = CustomUser.objects.create_user(
            username="testuser", email="test@example.com", password="password123"
        )
        self.member = mommy.make(
            "CustomUser", first_name="Mary", type=CustomUser.Types.REGULAR
        )
        self.other_user = mommy.make("users.CustomUser", first_name="John Doe")
        self.minute_template = mommy.make(
            "secretarial.MinuteTemplateModel",
            body="Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
        )
        self.minute = mommy.make(
            "secretarial.MeetingMinuteModel",
            body="Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
        )
        mommy.make(
            "treasury.MonthlyBalance",
            month=self.date_before,
        )
        mommy.make("MinuteExcerptsModel")
        self.transaction = TransactionModel.objects.create(
            user_id=1,
            description="Test Transaction1",
            amount=Decimal(str(300.00)),
            is_positive=True,
            date=self.date
        )

    def test_get_current_balance(self):
        TransactionModel.objects.create(
            user=self.user,
            description="Test Transaction",
            amount=Decimal(str(500.00)),
            date=self.date,
        )

        url = reverse("get-current-balance")
        self.client.force_login(self.user)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("current_balance", response.data)
        self.assertIn("last_month_balance", response.data)

    def test_transaction_cat_list(self):
        url = reverse("get-transactions")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Add assertions for the response data

    def test_create_transaction(self):
        url = reverse("post-transaction")
        data = {
            "user": 1,  # Replace with the appropriate user ID
            "category": None,  # Replace with the category ID if needed
            "description": "Test Transaction2",
            "amount": "200.00",
            "is_positive": True,
            "date": self.date,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_transaction_invalid_data(self):
        url = reverse("post-transaction")
        data = {
            # Invalid data here
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_transaction(self):
        url = reverse("delete-transaction", kwargs={"pk": self.transaction.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(TransactionModel.objects.filter(pk=self.transaction.pk).exists())

    def test_get_data(self):
        MinuteExcerptsModel.objects.create()

        url = reverse("get-data")
        self.client.force_login(self.user)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_detailed_data(self):
        pk = 1  # Replace with an existing PK
        url = reverse("get-detailed-data", kwargs={"pk": pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unified_search(self):
        url = reverse("secretarial-search")
        user_data = {"category": "users", "searched": "John Doe"}
        response = self.client.post(url, user_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        member_data = {"category": "members", "searched": "Rafael"}
        response = self.client.post(url, member_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        min_template_data = {"category": "templates", "searched": "Lorem"}
        response = self.client.post(url, min_template_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        minute_data = {"category": "minutes", "searched": "Lorem"}
        response = self.client.post(url, minute_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        invalid_data = {"category": "invalid", "searched": "Lorem"}
        response = self.client.post(url, invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
