from django.shortcuts import render , get_object_or_404
from django.http import HttpResponse
# Create your views here
from rest_framework import generics , views
from .  import serializers
from . import models
from rest_framework.response import Response
from rest_framework import authentication
from rest_framework import permissions
from rest_framework import status


class UsersAPIView(generics.ListAPIView):
    serializer_class = serializers.UserModelSerializer
    def get_queryset(self):
        return models.UserModel.objects.all().order_by('id')



class CategoryAPIView(generics.ListCreateAPIView):
    serializer_class = serializers.CategoryModelSerializer
    authentication_classes  = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly ]

    
    def get_queryset(self):
        return models.ProductCategory.objects.all().order_by('id')

    def post(self , request):
        serializer = serializers.CategoryModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(f'error')   
  


class CategoryDetailView(views.APIView):
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]
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


    

