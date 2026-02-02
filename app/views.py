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
from django.core.cache import cache
from rest_framework_simplejwt.authentication import JWTAuthentication

class UsersAPIView(generics.ListAPIView):
    serializer_class = serializers.UserModelSerializer
    def get_queryset(self):
        return models.UserModel.objects.all().order_by('id')



class CategoryAPIView(generics.ListCreateAPIView):
    serializer_class = serializers.CategoryModelSerializer
    authentication_classes  = [authentication.BasicAuthentication , JWTAuthentication ]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly ]
    CACHE_KEY=  'categories_cache'
    def get_queryset(self):
        return models.ProductCategory.objects.select_related('products').all()
    def list(self, request, *args, **kwargs):
        data = cache.get(self.CACHE_KEY)
        if data is None:
            response = super().list(request, *args, **kwargs)
            data = response.data
            cache.set(self.CACHE_KEY , data , 120)
            return response
        return Response(data)
    
    def perform_create(self, serializer):
        serializer.save()
        cache.delete(self.CACHE_KEY)
    
class CategoryDetailView(views.APIView):
    authentication_classes = [authentication.BasicAuthentication , authentication.SessionAuthentication , JWTAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    ALL_CATEGORIES_CACHE_KEY =  'categories_cache'
    def delete(self , request , *args , **kwargs ):
        
        pk= kwargs.get('id')
        CACHE_KEY=  f'category_detail_cache_{pk}'
        category = get_object_or_404(models.ProductCategory ,  pk=pk)
        category.delete()
        cache.delete(CACHE_KEY)
        cache.delete(self.ALL_CATEGORIES_CACHE_KEY)
        return Response('successfully deleted' , status.HTTP_404_NOT_FOUND) 


    def patch(self , request , *args , **kwargs):
        pk= kwargs.get('id')
        CACHE_KEY = f'category_detail_cache_{pk}'
        category = get_object_or_404(models.ProductCategory ,pk=pk)
        serializer = serializers.CategoryModelSerializer(instance=category  , partial = True ,  data=request.data)
        if serializer.is_valid():
            serializer.save()
            cache.delete(CACHE_KEY)
            cache.delete(self.ALL_CATEGORIES_CACHE_KEY)
            return Response('successfully patched')
        
        return Response('error')

    def get(self , request , *args , **kwargs):
        pk = kwargs.get('id')
        cache_key = f'category_detail_cache_{pk}'
        data = cache.get(cache_key  )
        if data is None:
            category = get_object_or_404(models.ProductCategory.objects.prefetch_related('products').all().order_by('id')  , pk=pk)
            serializer = serializers.CategoryModelSerializer(category)
            cache.set(cache_key , serializer.data , 120 )
            return Response(serializer.data ,  status.HTTP_200_OK)
        return Response(data , status.HTTP_200_OK)

            


class ProductAPIView(views.APIView):
      authentication_classes  = [authentication.BasicAuthentication , authentication.TokenAuthentication , JWTAuthentication ]
      permission_classes = [permissions.IsAuthenticatedOrReadOnly ]
      pagination_class =  CustomPagination
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
            
              return Response(status=status.HTTP_201_CREATED)
 
          return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)

class ProductDetailAPIView(views.APIView):
    authentication_classes =  [authentication.BasicAuthentication , authentication.TokenAuthentication ,  JWTAuthentication ]
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





class CommentModelAPIView(views.APIView):
    authentication_classes =  [authentication.BasicAuthentication , authentication.TokenAuthentication ,  JWTAuthentication ]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly ]

    pagination_class = CustomPagination
    def get(self , request  , *args ,  **kwargs):
          
           comments = models.CommentModel.objects.select_related('author').all()
           paginator = self.pagination_class()
           page = paginator.paginate_queryset(queryset=comments  , request=request)
           if page is not None:
              serializer =  serializers.CommentModelSerializer(page , many=True)
              return paginator.get_paginated_response(serializer.data)
           serializer = serializers.ProductModelSerializer(instance = comments , many=True) 
           return Response(serializer.data , status.HTTP_200_OK)
     
    def post(self , request , *args , **kwargs):

        serializer = serializers.CommentModelSerializer(data=request.data)
        if serializer.is_valid():
            author_id = request.data.get('author')
            author_obj = get_object_or_404(models.UserModel, id=author_id)
            serializer.save(author=author_obj)
            return Response('successfully created' , status.HTTP_200_OK)
        return Response(serializer.errors ,  status.HTTP_404_NOT_FOUND)
    

class CommentDetailAPIView(views.APIView):
    def patch(self,request , *args , **kwargs):
        pk = kwargs.get('id')
        comment = get_object_or_404(models.CommentModel  , pk=pk)
        serializer  = serializers.CommentModelSerializer(instance=comment ,  partial=True ,  data  = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status.HTTP_201_CREATED)
        return Response(serializer.errors , status.HTTP_400_BAD_REQUEST)
    

    def delete(self , request , *args , **kwargs):
        pk = kwargs.get('id')
        comment  = get_object_or_404(models.CommentModel , pk=pk)
        comment.delete()
        return Response('successfully deleted' ,  status.HTTP_202_ACCEPTED)
    

