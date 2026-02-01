from django.contrib import admin
from django.urls import path, include 
from . import views


urlpatterns = [
    path('api-auth/', include('rest_framework.urls') ,  name='rest'),
    path('api/users/' , views.UsersAPIView.as_view() ,  name='users_api_view'),
    path('api/categories/' , views.CategoryAPIView.as_view() , name = 'categories-api_view'),
    path('api/category/detail/<int:id>',views.CategoryDetailView.as_view() ,  name='category_detail_api_view'),
    path('api/products/' ,  views.ProductAPIView.as_view() , name='products_api_view'),
    path('api/product/detail/<int:id>' , views.ProductDetailAPIView.as_view() ,  name='product_detail_view')
    
]
