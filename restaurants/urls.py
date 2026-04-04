from django.urls import path
from . import views

app_name = 'restaurants'

urlpatterns = [
    path('', views.home, name='home'),
    path('restaurants/', views.restaurant_list, name='list'),
    path('restaurants/<int:id>/', views.restaurant_detail, name='detail'),
    path(
        'restaurants/<int:id>/review/',
        views.add_review,
        name='add_review',
    ),
    path(
        'restaurants/<int:id>/favorite/',
        views.toggle_favorite,
        name='toggle_favorite',
    ),
    path('profile/', views.user_profile, name='profile'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('restaurants/create/', views.create_restaurant, name='create_restaurant'),
    path('restaurants/<int:id>/edit/', views.edit_restaurant, name='edit_restaurant'),
    path(
        'restaurants/<int:id>/delete/',
        views.delete_restaurant,
        name='delete_restaurant',
    ),
]