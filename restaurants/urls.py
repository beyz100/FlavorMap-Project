from django.urls import path
from . import views

app_name = 'restaurants'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('restaurants/', views.restaurant_list_view, name='list'),
    path('restaurants/<int:id>/', views.restaurant_detail_view, name='detail'),
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
]