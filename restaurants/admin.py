from django.contrib import admin
from .models import Category, Location, Restaurant, MenuItem, Review, Favorite


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "category", "location", "price_range", "phone")
    list_filter = ("category", "location", "price_range")
    search_fields = ("name", "description", "address", "phone")


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "restaurant", "price")
    list_filter = ("restaurant",)
    search_fields = ("name", "description")


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "restaurant", "user", "rating", "parent", "created_at")
    list_filter = ("rating", "created_at", "restaurant")
    search_fields = ("comment", "user__username", "restaurant__name")


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "restaurant", "created_at")
    list_filter = ("created_at",)
    search_fields = ("user__username", "restaurant__name")