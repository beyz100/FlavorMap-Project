from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Location(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Restaurant(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='restaurants')
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, related_name='restaurants')
    description = models.TextField()
    address = models.CharField(max_length=255)

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

    def __str__(self):
        return f"{self.name} - {self.restaurant.name}"

class Review(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.restaurant.name} - {self.user.username}"