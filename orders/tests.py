from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from shop.models import Category, Product
from orders.models import Cart, CartItem

User = get_user_model()


class OrderTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='TestPass123!',
        )
        self.category = Category.objects.create(name='Valorant')
        self.product = Product.objects.create(
            category=self.category,
            title='Valorant Points 1000',
            price=500.00,
            currency_amount=1000,
            is_active=True,
        )
        self.client.force_authenticate(user=self.user)

    def test_cart_requires_auth(self):
        self.client.force_authenticate(user=None)
        response = self.client.get('/api/cart/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_cart(self):
        response = self.client.get('/api/cart/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_add_to_cart(self):
        response = self.client.post('/api/cart/', {
            'product_id': self.product.id,
            'quantity': 1,
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_inactive_product_to_cart(self):
        inactive = Product.objects.create(
            category=self.category,
            title='Inactive Product',
            price=100.00,
            currency_amount=100,
            is_active=False,
        )
        response = self.client.post('/api/cart/', {
            'product_id': inactive.id,
            'quantity': 1,
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_order_from_cart(self):
        self.client.post('/api/cart/', {
            'product_id': self.product.id,
            'quantity': 1,
        })
        response = self.client.post('/api/orders/')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], 'new')

    def test_create_order_empty_cart(self):
        Cart.objects.create(user=self.user)
        response = self.client.post('/api/orders/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_orders_list(self):
        response = self.client.get('/api/orders/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_orders_requires_auth(self):
        self.client.force_authenticate(user=None)
        response = self.client.get('/api/orders/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)