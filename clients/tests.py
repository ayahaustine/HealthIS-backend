from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Client
from programs.models import Program
from accounts.models import User

class ClientTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='doctor@example.com',
            name='Dr. Smith',
            password='testpass123'
        )
        self.program = Program.objects.create(
            name="HIV Care",
            created_by=self.user
        )
        self.client_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'date_of_birth': '1990-01-01',
            'gender': 'M',
            'county': 'Nairobi',
            'program_ids': [self.program.id]
        }
        self.client.force_authenticate(user=self.user)

    def test_create_client_with_programs(self):
        response = self.client.post(reverse('client-list'), self.client_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        client = Client.objects.get(id=response.data['id'])
        self.assertEqual(client.programs.count(), 1)
        self.assertEqual(client.programs.first().name, "HIV Care")

    def test_cant_assign_others_programs(self):
        other_user = User.objects.create_user(email='other@example.com', password='test123')
        other_program = Program.objects.create(name="TB Program", created_by=other_user)
        
        data = self.client_data.copy()
        data['program_ids'] = [other_program.id]
        response = self.client.post(reverse('client-list'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("You don't have permission", str(response.data))

    def test_client_filtering(self):
        Client.objects.create(
            first_name='Alice',
            last_name='Smith',
            date_of_birth='1985-05-15',
            gender='F',
            county='Mombasa',
            created_by=self.user
        )
        response = self.client.get(reverse('client-list') + '?search=mombasa')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)