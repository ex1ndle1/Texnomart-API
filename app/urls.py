from django.contrib import admin
from django.urls import path, include 
from . import views


urlpatterns = [
    path('api-auth/', include('rest_framework.urls') ,  name='rest'),
    path('api/users/' , views.UsersAPIView.as_view() ,  name='users_api_view'),
    path('api/categories/' , views.CategoryAPIView.as_view() , name = 'categories-api_view'),
    path('api/category/detail/delete/<int:id>',views.CategoryDetailView.as_view() ,  name='category_delete_api_view'),
    path('api/category/detail/patch/<int:id>' , views.CategoryDetailView.as_view() ,  name='category_patch_api_view')
    
]
