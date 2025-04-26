from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Enrollment
from clients.models import Client
from programs.models import Program
from accounts.models import User

class EnrollmentTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='doctor@example.com',
            name='Dr. Smith',
            password='testpass123'
        )
        self.client_obj = Client.objects.create(
            first_name='John',
            last_name='Doe',
            date_of_birth='1990-01-01',
            gender='M',
            created_by=self.user
        )
        self.program = Program.objects.create(
            name='HIV Care',
            created_by=self.user
        )
        self.enrollment_data = {
            'client': self.client_obj.id,
            'program': self.program.id,
            'status': 'ACTIVE'
        }
        self.client.force_authenticate(user=self.user)

    def test_create_enrollment(self):
        response = self.client.post(reverse('enrollment-list'), self.enrollment_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Enrollment.objects.count(), 1)
        self.assertEqual(Enrollment.objects.first().status, 'ACTIVE')

    def test_completion_date_auto_set(self):
        data = self.enrollment_data.copy()
        data['status'] = 'COMPLETED'
        response = self.client.post(reverse('enrollment-list'), data)
        self.assertIsNotNone(response.data['completed_date'])

    def test_cant_enroll_others_clients(self):
        other_user = User.objects.create_user(email='other@example.com', password='test123')
        other_client = Client.objects.create(
            first_name='Mary',
            last_name='Smith',
            date_of_birth='1985-05-15',
            gender='F',
            created_by=other_user
        )
        data = self.enrollment_data.copy()
        data['client'] = other_client.id
        response = self.client.post(reverse('enrollment-list'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
