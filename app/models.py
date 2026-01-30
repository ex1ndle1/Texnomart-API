from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.



class UserModel(AbstractUser):
      username =  models.CharField(max_length=40, null=False , blank=False , unique=True)
      def __str__(self):
          return self.username

class ProductCategory(models.Model):
    title = models.CharField(max_length=50 ,  blank=False)
    def __str__(self):
        return self.title





class ProductModel(models.Model):
    title = models.CharField(max_length=250 ,  blank=False , null=False)
    category = models.ForeignKey(ProductCategory ,  on_delete=models.CASCADE , related_name='product_category' , blank=False)
    price = models.DecimalField(max_digits=8 , decimal_places=2)



class CommentModel(models.Model):
    text  = models.TextField(max_length=1000 ,  null=False)
    product = models.ForeignKey(ProductModel , on_delete=models.CASCADE, related_name='comments')
    author =  models.ForeignKey(UserModel , on_delete=models.CASCADE  , related_name='author')
    created_at = models.DateTimeField(auto_now_add=True)

class ImageModel(models.Model):
      title = models.CharField(max_length=50)
      product = models.ForeignKey(ProductModel ,  on_delete=models.CASCADE , related_name='products' , null=False , blank=False )
      image = models.ImageField(upload_to='images/' , null=False ,  blank=False)
      created_at =models.DateTimeField(auto_now_add=True)


class OrderModel(models.Model):
     user = models.ForeignKey(UserModel ,  on_delete=models.CASCADE , related_name='orders' , null=False , blank=False )
     product = models.ForeignKey(ProductModel ,  on_delete=models.CASCADE , related_name='orders' , null=False , blank=False )
     created_at =models.DateTimeField(auto_now_add=True)
