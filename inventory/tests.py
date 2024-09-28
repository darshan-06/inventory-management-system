from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

from inventory.models import Item

class ItemAPITestCase(APITestCase):
    def setUp(self):
        # Register a user for JWT token testing
        self.register_url = reverse('register')
        self.token_url = reverse('token_obtain_pair')
        self.token_refresh_url = reverse('token_refresh')

        # Register and authenticate user to get JWT token
        self.user_data = {
            'username': 'testuser',
            'password': 'testpassword',
        }
        self.client.post(self.register_url, self.user_data, format='json')
        
        # Obtain JWT token
        response = self.client.post(self.token_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.access_token = response.data['access']
        self.refresh_token = response.data['refresh']

        # Create authorization header with JWT access token for all subsequent requests
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        # Create an initial item for testing
        self.item = Item.objects.create(
            name="Test Item",
            description="Test description",
            quantity=10,
            price=100.00
        )

    def test_create_item(self):
        # Data for creating a new item
        url = reverse('create_item')
        data = {
            "name": "New Item",
            "description": "New item description",
            "quantity": 5,
            "price": "50.00"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Item.objects.count(), 2)
        self.assertEqual(Item.objects.get(name="New Item").description, "New item description")

    def test_get_item(self):
        # Retrieve the item
        url = reverse('item_detail', args=[self.item.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.item.name)

    def test_update_item(self):
        # Update the existing item
        url = reverse('item_detail', args=[self.item.id])
        data = {
            "name": "Updated Item",
            "description": "Updated description",
            "quantity": 20,
            "price": "200.00"
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.item.refresh_from_db()
        self.assertEqual(self.item.name, "Updated Item")
        self.assertEqual(self.item.quantity, 20)

    def test_delete_item(self):
        # Delete the item
        url = reverse('item_detail', args=[self.item.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Item.objects.count(), 0)

    def test_refresh_token(self):
        # Test refreshing the JWT token
        response = self.client.post(self.token_refresh_url, {'refresh': self.refresh_token}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_create_item_with_expired_token(self):
        # Simulate an expired token by resetting credentials and omitting the token
        self.client.credentials()  # Clears the Authorization header
        url = reverse('create_item')
        data = {
            "name": "Unauthorized Item",
            "description": "Should not create without valid token",
            "quantity": 5,
            "price": "50.00"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
