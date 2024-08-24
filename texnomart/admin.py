from django.contrib import admin
from django.contrib.auth.models import User, Group as auth_group
from import_export.admin import ImportExportModelAdmin
from texnomart import models

admin.site.register(models.Image)
admin.site.unregister(models.User)
admin.site.unregister(auth_group)
# admin.site.register(models.Comment)
admin.site.register(models.Attribute)
admin.site.register(models.AttributeValue)
admin.site.register(models.ProductAttribute)


@admin.register(models.Category)
class CategoryModelAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ['category_name', 'slug']
    prepopulated_fields = {'slug': ('category_name',)}


@admin.register(models.Product)
class ProductModelAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ['product_name', 'slug']
    prepopulated_fields = {'slug': ('product_name',)}    

@admin.register(models.Comment)
class CommentModelAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ['user', 'message','product']    