from django import forms
from .models import Restaurant, MenuItem

class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ['name', 'category', 'location', 'description', 'address', 'phone', 'price_range', 'photo']

class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ['name', 'description', 'price']
