from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from treasury.models import MonthlyBalance


class TreasuryHomeViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="testuser", email="test@example.com", password="password123"
        )
        cls.treasury_group = Group.objects.create(name="treasury")
        cls.permission = Permission.objects.get(codename="view_transactionmodel")
        cls.treasury_group.permissions.add(cls.permission)
        cls.user.groups.add(cls.treasury_group)

        # You may need to create MonthlyBalance instances as per your requirement
""" 
    def test_treasury_home_view(self):
        url = reverse("treasury:home")
        self.client.login(username="testuser", password="password123")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "treasury/home.html")

        # Add more specific assertions based on context data and expected behavior
        # For example:
        self.assertIn(
            "form_transaction", response.context
        )
 """