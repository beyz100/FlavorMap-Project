from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg

class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Location(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Restaurant(models.Model):
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='owned_restaurants')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='restaurants')
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, related_name='restaurants')
    description = models.TextField()
    address = models.CharField(max_length=255)

    PRICE_CHOICES = [
        ('1', '₺'),
        ('2', '₺₺'),
        ('3', '₺₺₺'),
    ]

    phone = models.CharField(max_length=20, blank=True, null=True)
    price_range = models.CharField(max_length=1, choices=PRICE_CHOICES, default='2')
    photo = models.ImageField(upload_to='restaurant_photos/', blank=True, null=True)

    def __str__(self):
        return self.name

    def average_rating(self):
        avg = self.reviews.aggregate(Avg('rating'))['rating__avg']
        if avg is not None:
            return round(avg, 1)
        return 0.0

class MenuItem(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='menu_items')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.CharField(max_length=50, blank=True, help_text="e.g., Starters, Main Course, Dessert")

    class Meta:
        verbose_name_plural = "Menu Items"

    def __str__(self):
        return f"{self.name} - {self.restaurant.name}"

class Review(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)], null=True, blank=True)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['restaurant', 'user'],
                condition=models.Q(parent__isnull=True),
                name='unique_main_review_per_user_per_restaurant'
            )
        ]

    def __str__(self):
        return f"{self.restaurant.name} - {self.user.username}"


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favorites")
    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, related_name="favorited_by"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "restaurant"],
                name="unique_favorite_user_restaurant",
            )
        ]

    def __str__(self):
        return f"{self.user.username} → {self.restaurant.name}"


class OpeningHours(models.Model):
    DAY_CHOICES = [
        ('weekdays', 'Weekdays'),
        ('weekends', 'Weekends'),
    ]
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='opening_hours')
    day = models.CharField(max_length=20, choices=DAY_CHOICES)
    open_time = models.TimeField()
    close_time = models.TimeField()

    class Meta:
        ordering = ['day']
        unique_together = ('restaurant', 'day')

    def __str__(self):
        return f"{self.restaurant.name} - {self.get_day_display()}"

class RestaurantPhoto(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='gallery_photos')
    image = models.ImageField(upload_to='restaurant_gallery/')
    caption = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Photo for {self.restaurant.name}"

