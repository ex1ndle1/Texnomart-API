from django.contrib import admin
from . import models
# Register your models here.


@admin.register(models.UserModel)
class UserAdminPanel(admin.ModelAdmin):
    list_per_page = 5

admin.site.register(models.ProductCategory)
admin.site.register(models.ProductModel)
admin.site.register(models.CommentModel)
admin.site.register(models.UserOrderModel)