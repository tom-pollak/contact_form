from django.test import TestCase
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework import status

from tiers.models import Tier

class UsersManagersTest(TestCase):
    def setUp(self):
        self.tier_free = Tier.objects.create(pk=1, name="Free", no_forms=5, price=0.00)
        self.tier_intermediate = Tier.objects.create(pk=2, name="Intermediate", no_forms=50, price=2.49)
        self.tier_unlimited = Tier.objects.create(pk=3, name="Unlimited", no_forms=2147483647, price=4.99)

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(email='normal@user.com', password='foo')
        self.assertEqual(str(user), 'normal@user.com')
        self.assertEqual(user.email, 'normal@user.com')

        self.assertEqual(user.tier.name, 'Free')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

        # username is None for the AbstractUser
        self.assertIsNone(user.username)

        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(email='')
        with self.assertRaises(ValueError):
            User.objects.create_user(email='', password='foo')

        with self.assertRaises(ValueError):
            User.objects.create_user(email='', password='foo', tier='Free')
        with self.assertRaises(ValueError):
            User.objects.create_user(email='', password='foo', tier=self.tier_free)
    
    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(email='super@user.com', password='foo')
        self.assertEqual(admin_user.email, 'super@user.com')

        self.assertEqual(admin_user.tier.name, 'Unlimited')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        self.assertIsNone(admin_user.username)

        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email='super@user.com', password='foo', is_superuser=False)
        
        with self.assertRaises(ValueError):
            User.objects.create_superuser(email='', password='foo', tier=self.tier_unlimited)

#TODO
class UserAPITest(APITestCase):
    def test_create_user(self):
        pass