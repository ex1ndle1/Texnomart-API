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
    product = ProductModelSerializer(many=True,read_only = True)
    class Meta:
        model  = models.ProductCategory
        fields = ('id','title' , 'product' )


class ImageModelSerializer(serializers.ModelSerializer):
    product = ProductModelSerializer( read_only= True)
    class Meta:
        model  = models.ImageModel
        fields = ('id' , 'title' , 'image' , 'created_at', 'product' )


class UserOrderModelSerializer(serializers.ModelSerializer):
    product_details = ProductModelSerializer(source='product', read_only=True)
    user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = models.UserOrderModel
        fields = ('id', 'user', 'product', 'product_details', 'created_at')
       
