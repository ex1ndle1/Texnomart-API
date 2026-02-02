from rest_framework import serializers
from . import models



class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserModel
        fields = ( 'username' , 'is_staff' , 'is_active')


class CommentModelSerializer(serializers.ModelSerializer):
    # author = serializers.ReadOnlyField(source='author.username' ,read_only=True)
    author = UserModelSerializer(read_only=True)
    class Meta:
        model  = models.CommentModel
        fields = ('id' , 'text' , 'product','author' ,'created_at' )


class ProductModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductModel
        fields = ('id' , 'title' , 'price'  , 'category')
    
class CategoryModelSerializer(serializers.ModelSerializer):
    products = ProductModelSerializer(many=True,read_only = True)
    class Meta:
        model  = models.ProductCategory
        fields = ('id','title' , 'products' )


