from django import forms
from .models import OpeningHours, Restaurant, MenuItem, Review, RestaurantPhoto

class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ['name', 'category', 'location', 'description', 'address', 'phone', 'price_range', 'photo', 'google_maps_embed_url']

class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ['name', 'category', 'description', 'price']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['comment']

class OpeningHoursForm(forms.ModelForm):
    class Meta:
        model = OpeningHours
        fields = ["day", "open_time", "close_time"]

class RestaurantPhotoForm(forms.ModelForm):
    class Meta:
        model = RestaurantPhoto
        fields = ['image', 'caption']
