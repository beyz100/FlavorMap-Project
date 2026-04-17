from django import forms
from .models import Restaurant, MenuItem, Review

class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ['name', 'category', 'location', 'description', 'address', 'phone', 'price_range', 'photo']

class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ['name', 'description', 'price']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['comment']
