from django.contrib import admin
from .models import Category_of_goods,Product_List


# Register your models here.

@admin.register(Category_of_goods)
class Category_of_goodsAdmin(admin.ModelAdmin):
    list_display = ('id','Name','Describe','Picture')

@admin.register(Product_List)
class Category_of_goodsAdmin(admin.ModelAdmin):
    list_display = ('id','Name', 'Picture','Category','vlaue','create_time','change_time')
    list_editable = ('Name','vlaue')
    list_per_page = 5