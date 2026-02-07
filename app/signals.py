
from django.db.models.signals import post_delete, post_save
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
import cloudinary.uploader
from . import models  
from django.db.models.signals import ModelSignal
import os
from django.core.cache import cache


@receiver(post_delete, sender=models.ImageModel)
def delete_image_from_cloudinary(sender, instance, **kwargs):
    
    if instance.image:
            file_path = instance.image.name
            public_id = os.path.splitext(file_path)[0]
            cloudinary.uploader.destroy(public_id)
            print(f"deleted from {public_id}")

@receiver([post_save , post_delete] , sender=models.ProductCategory )
def delete_category_cache( **kwargs):
      categories_cache = 'categories_cache'
      category_title  = kwargs.get('instance')
      category_detail_cache = f'category_detail_cache_{category_title}'
      cache.delete(category_detail_cache)
      cache.delete(categories_cache)



