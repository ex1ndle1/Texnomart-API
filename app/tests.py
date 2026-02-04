from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import ProductCategory
# Create your tests here.


class CategoryAPITest(TestCase):
    def setUp(self):
        self.url = reverse('categories-api_view')
    
    def test_get_categories(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)