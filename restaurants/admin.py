from django.contrib import admin
from .models import (
    Category,
    Favorite,
    Location,
    OpeningHours,
    Restaurant,
    MenuItem,
    Review,
    RestaurantPhoto,
)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class RestaurantPhotoInline(admin.TabularInline):
    model = RestaurantPhoto
    extra = 1

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'category', 'location', 'average_rating')
    list_filter = ('category', 'location')
    search_fields = ('name', 'description')
    inlines = [RestaurantPhotoInline]

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'restaurant', 'price')
    list_filter = ('restaurant',)
    search_fields = ('name',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('restaurant', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('restaurant__name', 'user__username', 'comment')


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'restaurant', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('restaurant__name', 'user__username')


@admin.register(OpeningHours)
class OpeningHoursAdmin(admin.ModelAdmin):
    list_display = ('restaurant', 'day', 'open_time', 'close_time')
    list_filter = ('day',)