from django.test import TestCase
from django.contrib.auth import get_user_model
from users.models import UsersFunctions, CustomUser


class CustomUserTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(
            username="testuser",
            first_name="Test",
            last_name="User",
        )
        self.user.set_password("testpassword")
        self.user.save()
        self.function = UsersFunctions.objects.create(function="P")

    def test_custom_user_creation(self):
        self.assertEqual(self.user.username, "testuser")
        self.assertEqual(self.user.first_name, "Test")
        self.assertEqual(self.user.last_name, "User")
        self.assertTrue(self.user.check_password("testpassword"))

    def test_users_functions_creation(self):
        self.assertEqual(self.function.function, "P")

    def test_user_type_upgrade(self):
        self.user.functions.add(self.function)
        self.user.save()
        self.user.type = CustomUser.Types.STAFF
        self.user.save()
        self.assertEqual(self.user.type, CustomUser.Types.STAFF)

    def test_user_marriage(self):
        # Create another user
        spouse = get_user_model().objects.create(
            username="spouseuser",
            first_name="Spouse",
            last_name="User",
        )
        # Set the marriage information
        self.user.married_to = spouse
        self.user.date_of_marriage = "2023-10-20"
        self.user.save()
        self.assertEqual(self.user.married_to, spouse)
        self.assertEqual(self.user.date_of_marriage, "2023-10-20")

    def test_user_phone_number(self):
        phone_number = "+1234567890"
        self.user.phone_number = phone_number
        self.user.save()
        self.assertEqual(self.user.phone_number, phone_number)
