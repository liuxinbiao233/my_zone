
from django.urls import path
from product import views


urlpatterns=[
    path('',views.product_list,name='product_list'),
    path('<int:product_pk>/',views.product_detail,name='product_detail'),
    path('type/<int:Category_pk>',views.Category,name="Category"),
    path('date/<int:year>/<int:month>/<int:day>',views.product_date,name='product_date'),
    path('type/2', views.Category, name='Category_mobile'),
    path('type/1', views.Category, name='Category_computer'),
    path('type/3', views.Category, name='Category_shoes'),
    path('type/4', views.Category, name='Category_Personal_modeling'),
    path('type/6', views.Category, name='Category_Headset'),
]