from django.shortcuts import render , get_object_or_404
from django.http import HttpResponse
# Create your views here
from rest_framework import generics , views
from .  import serializers
from . import models
from .paginations import CustomPagination
from rest_framework.response import Response
from rest_framework import authentication
from rest_framework import permissions
from rest_framework import status
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.core.cache import cache


class UsersAPIView(generics.ListAPIView):
    serializer_class = serializers.UserModelSerializer
    def get_queryset(self):
        return models.UserModel.objects.all().order_by('id')



class CategoryAPIView(generics.ListCreateAPIView):
    serializer_class = serializers.CategoryModelSerializer
    authentication_classes  = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly ]
    CACHE_KEY=  'categories_cache'
    def get_queryset(self):
        return models.ProductCategory.objects.all().order_by('id')
    
    def list(self, request, *args, **kwargs):
        data = cache.get(self.CACHE_KEY)
        if data is None:
            response = super().list(request, *args, **kwargs)
            data = response.data
            cache.set(self.CACHE_KEY , data , 120)
            print('hi')
            return response
        print('hip')
        return Response(data)
    def perform_create(self, serializer):
        serializer.save()
        cache.delete(self.CACHE_KEY)
    
class CategoryDetailView(views.APIView):
    authentication_classes = [authentication.BasicAuthentication , authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    CACHE_KEY=  'category_detail_cache'
    def delete(self , request , *args , **kwargs ):
        pk= kwargs.get('id')
        category = get_object_or_404(models.ProductCategory ,  pk=pk)
        category.delete()
        return Response('successfully deleted' , status.HTTP_404_NOT_FOUND) 


    def patch(self , request , *args , **kwargs):
        pk= kwargs.get('id')
        category = get_object_or_404(models.ProductCategory ,pk=pk)
        serializer = serializers.CategoryModelSerializer(instance=category  , partial = True ,  data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response('successfully patched')
        return Response('error')

    def get(self , request , *args , **kwargs):
        pk = kwargs.get('id')
        category = get_object_or_404(models.ProductCategory.objects.prefetch_related('products').all().order_by('id')  , pk=pk)
        serializer = serializers.CategoryModelSerializer(category)
        
        return Response(serializer.data , status.HTTP_200_OK)

            


class ProductAPIView(views.APIView):
      authentication_classes  = [authentication.BasicAuthentication , authentication.TokenAuthentication ]
      permission_classes = [permissions.IsAuthenticatedOrReadOnly ]
      pagination_class =  CustomPagination
      CACHE_KEY=  'products_cache'
      def get(self ,  request , *args ,**kwargs): 
          products  = models.ProductModel.objects.all().order_by('id')
          paginator = self.pagination_class()
          page = paginator.paginate_queryset(queryset=products , request=request)
          if page is not None:
              serializer = serializers.ProductModelSerializer(page , many=True)
              return paginator.get_paginated_response(serializer.data)
          serializer = serializers.ProductModelSerializer(instance = products , many=True)
          return Response(serializer.data , status.HTTP_200_OK)
      
      def post(self , request , *args , **kwargs):
          serializer   =  serializers.ProductModelSerializer(data=request.data)
          if serializer.is_valid():
              serializer.save()
              cache.delete('categories_data')
              return Response(status=status.HTTP_201_CREATED)
          cache.delete(self.CACHE_KEY)
          return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)
          

class ProductDetailAPIView(views.APIView):
    authentication_classes =  [authentication.BasicAuthentication , authentication.TokenAuthentication ]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly ]

    def patch(self , request , *args , **kwargs):
        pk  = kwargs.get('id')
        product = get_object_or_404(models.ProductModel , pk=pk)
        serializer =  serializers.ProductModelSerializer(instance=product , partial=True , data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response('successfully patched'  , status=status.HTTP_202_ACCEPTED)
        return Response('error' ,  status.HTTP_404_NOT_FOUND)
    

    def delete(self , request , *args , **kwargs ):
        pk = kwargs.get('id')
        product = get_object_or_404(models.ProductModel ,  pk=pk)
        product.delete()
        
        return Response('successfully deleted' ,  status.HTTP_200_OK)
    
    



