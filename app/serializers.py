from rest_framework import serializers
from . import models



class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserModel
        fields = ('id' ,  'username' , 'is_staff' , 'is_active')


class ProductModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductModel
        fields = ('id' , 'title' , 'price' )
    
class CategoryModelSerializer(serializers.ModelSerializer):
    products = ProductModelSerializer(many=True)
    def create(self , validatedata):
        return  models.ProductCategory.objects.create(**validatedata)


    class Meta:
        model  = models.ProductCategory
        fields = ('id','title' , 'products' )