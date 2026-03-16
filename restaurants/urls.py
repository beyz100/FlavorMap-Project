from django.urls import path
from . import views

app_name = 'restaurants'

urlpatterns = [
    path('', views.home, name='home'),
    path('restaurants/', views.restaurant_list, name='list'),
    path('restaurants/<int:id>/', views.restaurant_detail, name='detail'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('restaurants/create/', views.create_restaurant, name='create_restaurant'),
    path('<int:id>/edit/', views.edit_restaurant, name='edit_restaurant'),
]