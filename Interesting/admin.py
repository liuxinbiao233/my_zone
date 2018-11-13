from django.contrib import admin

# Register your models here.
from Interesting.models import Type, Interesting


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ('id','type')

@admin.register(Interesting)
class InterestingAdmin(admin.ModelAdmin):
    list_display = ('id','things','type','content','create_time')
