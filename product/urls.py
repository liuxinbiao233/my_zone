
from django.urls import path
from product import views


urlpatterns=[
    path('',views.product_list,name='product_list'),
    path('<int:product_pk>/',views.product_detail,name='product_detail'),
    path('type/<int:Category_pk>',views.Category,name="Category"),
]