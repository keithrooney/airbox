from django.test import TestCase

from airbox.iam.models import User


class UserTest(TestCase):

    def test_create_user(self):
        user = User.objects.create_user(email='johndoe@foobar.com', password='password1234!.', first_name='John', last_name='Doe')
        other = User.objects.get(email=user.email)
        self.assertEqual(user, other)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        user = User.objects.create_superuser(email='johndoe@foobar.com', password='password1234!.', first_name='John', last_name='Doe')
        other = User.objects.get(email=user.email)
        self.assertEqual(user, other)
        self.assertTrue(user.is_superuser)
