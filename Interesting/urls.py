from django.urls import path
from Interesting import views

urlpatterns = [
    path('', views.insteresting_list, name='insterering_list'),
    path('<int:things_pk>/', views.things_detail, name='things_detail'),
]