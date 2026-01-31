from django.shortcuts import render
from django.http import HttpResponse
# Create your views here
from rest_framework import generics , views
from .  import serializers
from . import models
from rest_framework.response import Response
from rest_framework import authentication
from rest_framework import permissions



class UsersAPIView(generics.ListAPIView):
    serializer_class = serializers.UserModelSerializer
    def get_queryset(self):
        return models.UserModel.objects.all().order_by('id')
    
class CategoryAPIView(generics.ListAPIView):
    serializer_class = serializers.CategoryModelSerializer
    authentication_classes  = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly ]

    
    def get(self,request, *args, **kwargs):
        categories = models.ProductCategory.objects.all()
        return Response(serializers.CategoryModelSerializer(categories ,  many=True).data)
    
    def post(self , request):
        serializer = serializers.CategoryModelSerializer(data=request.data)
        
        models.ProductCategory.objects.create(title=request.data['title'])
            
        return Response('created succecfully')    
    
class CategoryDetailView(views.APIView):
    def delete(self , request , *args , **kwargs ):
        pass