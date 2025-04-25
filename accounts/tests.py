# apps/accounts/tests.py
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

User = get_user_model()

class UserModelTests(APITestCase):
    def test_create_user(self):
        user = User.objects.create_user(
            email='test@example.com',
            name='Test User',
            password='testpass123'
        )
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.name, 'Test User')
        self.assertTrue(user.check_password('testpass123'))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertIsNone(user.username)

    def test_create_superuser(self):
        admin_user = User.objects.create_superuser(
            email='admin@example.com',
            name='Admin User',
            password='adminpass123'
        )
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)

class RegistrationTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('auth_register')

    def test_successful_registration(self):
        data = {
            'email': 'user@example.com',
            'name': 'Test User',
            'password': 'securepassword123'
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        user = User.objects.get()
        self.assertEqual(user.email, 'user@example.com')
        self.assertTrue(user.check_password('securepassword123'))

    def test_registration_with_missing_data(self):
        data = {'email': 'invalid@example.com'}
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)

    def test_duplicate_email_registration(self):
        User.objects.create_user(
            email='existing@example.com',
            name='Existing User',
            password='testpass123'
        )
        data = {
            'email': 'existing@example.com',
            'name': 'New User',
            'password': 'newpass123'
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class LoginTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.login_url = reverse('token_obtain')
        self.user = User.objects.create_user(
            email='testuser@example.com',
            name='Test User',
            password='testpass123'
        )

    def test_successful_login(self):
        data = {
            'email': 'testuser@example.com',
            'password': 'testpass123'
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_invalid_credentials(self):
        data = {
            'email': 'testuser@example.com',
            'password': 'wrongpassword'
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)



class LogoutTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.logout_url = reverse('auth_logout')
        self.user = User.objects.create_user(
            email='testuser@example.com',
            name='Test User',
            password='testpass123'
        )
        refresh = RefreshToken.for_user(self.user)
        self.valid_refresh = str(refresh)
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}'
        )

    def test_successful_logout(self):
        data = {'refresh': self.valid_refresh}
        response = self.client.post(self.logout_url, data)
        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)
        
        with self.assertRaises(TokenError) as context:
            RefreshToken(self.valid_refresh).check_blacklist()
        
        self.assertIn('blacklisted', str(context.exception))

    def test_logout_with_invalid_token(self):
        data = {'refresh': 'invalid_token'}
        response = self.client.post(self.logout_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class ProfileTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            name='Test User',
            password='testpass123'
        )
        self.client = APIClient()
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def test_get_profile(self):
        response = self.client.get(reverse('user_profile'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'test@example.com')
        self.assertEqual(response.data['name'], 'Test User')

    def test_unauthenticated_access(self):
        self.client.credentials()
        response = self.client.get(reverse('user_profile'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
