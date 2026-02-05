from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import ProductCategory
from django.contrib.auth.models import User
from . import models
# Create your tests here.


class CategoryAPITest(TestCase):
    def setUp(self):
        self.url = reverse('categories_api_view')
    
    def test_get_categories(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    


class ProductAPITest(TestCase):
    def setUp(self):
        
        self.user  =  models.UserModel.objects.create(username='muza12' , password='123')
        self.category = models.ProductCategory.objects.create(title='phones')
        self.product =  models.ProductModel.objects.create(title='iphonus' , category=self.category , price='1233')
        self.url = reverse('products_api_view' )
    def test_get_producs(self):
        self.client.force_login(user=self.user)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code , status.HTTP_200_OK)



class ProductAPIDetailTest(TestCase):
    def setUp(self):
        self.user = models.UserModel.objects.create_user(username='muza12', password='123')
        self.category = models.ProductCategory.objects.create(title='phones')
        self.product = models.ProductModel.objects.create(title='iphonus', category=self.category, price= 1233 )
        self.url = reverse('product_detail_api_view', kwargs={'id': self.product.pk})
        
    def test_product_delete(self):
        self.client.force_login(user=self.user)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code , status.HTTP_204_NO_CONTENT)

    
