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
    PRICE_CHOICES = [
        ('$', '$'),
        ('$$', '$$'),
        ('$$$', '$$$'),
    ]

    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='restaurants')
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, related_name='restaurants')
    description = models.TextField()
    address = models.CharField(max_length=255)

    phone = models.CharField(max_length=20, blank=True)
    price_range = models.CharField(max_length=3, choices=PRICE_CHOICES, default='$')
    map_embed_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

    def average_rating(self):
        avg = self.reviews.filter(parent__isnull=True).aggregate(Avg('rating'))['rating__avg']
        if avg is not None:
            return round(avg, 1)
        return 0.0


class MenuItem(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='menu_items')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)

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
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['restaurant', 'user', 'parent'],
                condition=models.Q(parent__isnull=True),
                name='unique_main_review_per_user_per_restaurant'
            )
        ]
        ordering = ['-created_at']

    def __str__(self):
        if self.parent:
            return f"Reply by {self.user.username} on {self.restaurant.name}"
        return f"{self.restaurant.name} - {self.user.username}"

    def is_reply(self):
        return self.parent is not None


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'restaurant'],
                name='unique_favorite_per_user_restaurant'
            )
        ]
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} likes {self.restaurant.name}"