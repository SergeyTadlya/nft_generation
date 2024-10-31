from django.contrib import admin
from .models import *


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'type', 'folder_name']
    list_filter = ['type']
    readonly_fields = ['created_on']


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'image']
    list_filter = ['collection_type']
    readonly_fields = ['uploaded_on']