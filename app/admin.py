from django.contrib import admin
from . import models
# Register your models here.


@admin.register(models.User)
class UserAdminPanel(admin.ModelAdmin):
    list_per_page = 5