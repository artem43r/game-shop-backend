from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from shop.models import Category, Product

User = get_user_model()


class ShopTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.category = Category.objects.create(name='Valorant')
        self.product = Product.objects.create(
            category=self.category,
            title='Valorant Points 1000',
            price=500.00,
            currency_amount=1000,
            is_active=True,
        )
        self.admin = User.objects.create_superuser(
            username='admin',
            email='admin@test.com',
            password='AdminPass123!',
        )

    def test_categories_public(self):
        response = self.client.get('/api/categories/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_products_public(self):
        response = self.client.get('/api/products/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_products_search(self):
        response = self.client.get('/api/products/?search=Valorant')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_products_filter_by_category(self):
        response = self.client.get(f'/api/products/?category={self.category.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_product_unauthorized(self):
        response = self.client.post('/api/products/', {
            'title': 'Test',
            'price': 100,
            'currency_amount': 100,
            'category': self.category.id,
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_product_as_admin(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.post('/api/products/', {
            'title': 'New Product',
            'price': 100.00,
            'currency_amount': 500,
            'category': self.category.id,
            'is_active': True,
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_product_as_regular_user(self):
        user = User.objects.create_user(
            username='regular',
            email='regular@test.com',
            password='Pass123!',
        )
        self.client.force_authenticate(user=user)
        response = self.client.post('/api/products/', {
            'title': 'Test',
            'price': 100,
            'currency_amount': 100,
            'category': self.category.id,
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)