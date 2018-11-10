from django.contrib import admin
from .models import Blog_Type, Blog

# Register your models here.

@admin.register(Blog_Type)
class Blog_TypeAdmin(admin.ModelAdmin):
    list_display = ('id','type_name')

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'blog_type','author','get_read_num','create_time','last_charge_time')
    list_editable = ('title','author')
    list_per_page = 5
    #'length'这个是内容的长度
