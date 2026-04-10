from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Restaurant, Category, Location, Favorite


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

    is_favorited = False
    if request.user.is_authenticated:
        is_favorited = Favorite.objects.filter(
            user=request.user,
            restaurant=restaurant
        ).exists()

    context = {
        'restaurant': restaurant,
        'menu_items': menu_items,
        'reviews': reviews,
        'is_favorited': is_favorited,
    }
    return render(request, 'restaurants/detail.html', context)


@login_required
def toggle_favorite(request, id):
    restaurant = get_object_or_404(Restaurant, id=id)

    favorite = Favorite.objects.filter(
        user=request.user,
        restaurant=restaurant
    ).first()

    if favorite:
        favorite.delete()
    else:
        Favorite.objects.create(user=request.user, restaurant=restaurant)

    return redirect('restaurants:restaurant_detail', id=restaurant.id)


def about(request):
    return render(request, 'restaurants/about.html')


def contact(request):
    return render(request, 'restaurants/contact.html')