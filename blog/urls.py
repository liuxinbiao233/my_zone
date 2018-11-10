from django.urls import path
from blog import views


urlpatterns=[
    path('',views.home,name='blog_name'),
    path('blog/',views.blog_list,name='blog_list'),
    path('<int:blog_pk>/',views.blog_detail,name='blog_detail'),
    path('type/<int:blog_type_pk>',views.blog_type,name="blog_type"),
    path('date/<int:year>/<int:month>/<int:day>',views.blog_date,name='blog_date'),
    path('type/1',views.blog_type,name='blog_type_scrapy'),
    path('type/2',views.blog_type,name='blog_type_tools'),
    path('type/3',views.blog_type,name='blog_type_opencv'),
    path('type/4',views.blog_type,name='blog_type_hadhoop'),
]