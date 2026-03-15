from django.shortcuts import render, get_object_or_404
from .models import Restaurant, Category, Location

def home(request):
    featured_restaurants = Restaurant.objects.all().order_by('-id')[:3]
    return render(request, 'restaurants/home.html', {'restaurants': featured_restaurants})

def restaurant_list(request):
    restaurants = Restaurant.objects.all()
    return render(request, 'restaurants/list.html', {'restaurants': restaurants})

def restaurant_detail(request, id):
    restaurant = get_object_or_404(Restaurant, id=id)
    
    menu_items = restaurant.menu_items.all()
    reviews = restaurant.reviews.all().order_by('-created_at')
    
    context = {
        'restaurant': restaurant,
        'menu_items': menu_items,
        'reviews': reviews,
    }
    return render(request, 'restaurants/detail.html', context)

def about(request):
    return render(request, 'restaurants/about.html')

def contact(request):
    return render(request, 'restaurants/contact.html')