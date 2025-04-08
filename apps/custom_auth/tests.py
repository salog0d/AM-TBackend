from django.test import TestCase

from custom_auth.models import CustomUser

# Create your tests here.
class CustomAuthTests(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create(
            username="testuser", 
            password="testpassword", 
            email="david.salomon.nava11@gmail.com",
            role="admin",
            discipline="investigation",
            date_of_birth="2000-01-01",
            phone_number="1234567890",
        )

    def test_user_creation(self):
        user = CustomUser.objects.get(username="testuser")
        self.assertEqual(user.email, "david.salomon.nava11@gmail.com")
        self.assertEqual(user.role, "admin")
        self.assertEqual(user.discipline, "investigation")
        self.assertEqual(user.date_of_birth.strftime("%Y-%m-%d"), "2000-01-01")
        self.assertEqual(user.phone_number, "1234567890")

