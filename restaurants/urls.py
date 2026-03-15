from django.urls import path
from . import views

app_name = 'restaurants'

urlpatterns = [
    path('', views.home, name='home'),
    path('restaurants/', views.restaurant_list, name='list'),
    path('restaurants/<int:id>/', views.restaurant_detail, name='detail'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
]