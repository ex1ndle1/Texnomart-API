from django.contrib import admin
from . import models
# Register your models here.


@admin.register(models.UserModel)
class UserAdminPanel(admin.ModelAdmin):
    list_per_page = 5

admin.site.register(models.ProductCategory)

@admin.register(models.ProductModel)
class ProductModelAdminPanel(admin.ModelAdmin):
    list_per_page  = 50

@admin.register(models.CommentModel)
class CommentModelAminPanel(admin.ModelAdmin):
    list_per_page = 50

@admin.register(models.ImageModel)
class ImageModelAdminPanel(admin.ModelAdmin):
    list_per_page = 50



