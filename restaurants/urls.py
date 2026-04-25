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
    path('restaurants/<int:id>/delete/', views.delete_restaurant, name='delete_restaurant'),
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
    path('restaurants/<int:id>/menu/add/', views.add_menu_item, name='add_menu_item'),
    path('menu/<int:id>/delete/', views.delete_menu_item, name='delete_menu_item'),
    path('menu/<int:id>/edit/', views.edit_menu_item, name='edit_menu_item'),
    path("reviews/<int:id>/edit/", views.edit_review, name="edit_review"),
    path("reviews/<int:id>/delete/", views.delete_review, name="delete_review"),
    path("reviews/<int:id>/reply/", views.add_reply, name="add_reply"),
    path('restaurants/<int:restaurant_id>/opening-hours/add/', views.add_opening_hours, name='add_opening_hours'),
    path('opening-hours/<int:id>/edit/', views.edit_opening_hours, name='edit_opening_hours'),
    path('opening-hours/<int:id>/delete/', views.delete_opening_hours, name='delete_opening_hours'),
    path('restaurants/<int:restaurant_id>/photos/add/', views.add_photo, name='add_photo'),
    path('photos/<int:id>/delete/', views.delete_photo, name='delete_photo'),
]