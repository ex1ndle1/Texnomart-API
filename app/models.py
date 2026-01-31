from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class UserModel(AbstractUser):
    username = models.CharField(max_length=40, unique=True)
    
    def __str__(self):
        return self.username

class ProductCategory(models.Model):
    title = models.CharField(max_length=50)
    
    def __str__(self):
        return self.title

class ProductModel(models.Model):
    title = models.CharField(max_length=250)
    category = models.ForeignKey(
        ProductCategory, 
        on_delete=models.CASCADE, 
        related_name='products'
    )
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.title

class CommentModel(models.Model):
    text = models.TextField(max_length=1000)
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='comments'
    )
    created_at = models.DateTimeField(auto_now_add=True)

class ImageModel(models.Model):
    title = models.CharField(max_length=50)
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='images/')
    created_at = models.DateTimeField(auto_now_add=True)

class UserOrderModel(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,  on_delete=models.CASCADE,         related_name='orders'    )
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, related_name='user_orders')
    created_at = models.DateTimeField(auto_now_add=True)