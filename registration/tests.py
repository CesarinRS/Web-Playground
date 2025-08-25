from django.test import TestCase
from .models import Profile
from django.contrib.auth.models import User

# Create your tests here.
class ProfileTestCase(TestCase):
    def setUp(self):
        User.objects.create_user(username='test', email='tester@test.com', password='Tester123')

    def test_profile_exists(self):
        exists = Profile.objects.filter(user__username='test').exists()
        self.assertTrue(exists, True)

