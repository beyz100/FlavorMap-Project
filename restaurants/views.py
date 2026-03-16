from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
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
    

@login_required
def create_restaurant(request):
    if request.method == "POST":
        name = request.POST.get("name")
        category_id = request.POST.get("category")
        location_id = request.POST.get("location")
        description = request.POST.get("description")
        address = request.POST.get("address")

        restaurant = Restaurant.objects.create(
            name=name,
            category_id=category_id,
            location_id=location_id,
            description=description,
            address=address
        )

        return redirect("restaurants:detail", id=restaurant.id)

    categories = Category.objects.all()
    locations = Location.objects.all()

    context = {
        "categories": categories,
        "locations": locations
    }

    return render(request, "restaurants/create_restaurant.html", context)
    
    
@login_required
def edit_restaurant(request, id):
    restaurant = get_object_or_404(Restaurant, id=id)

    if request.method == "POST":
        restaurant.name = request.POST.get("name")
        restaurant.category_id = request.POST.get("category")
        restaurant.location_id = request.POST.get("location")
        restaurant.description = request.POST.get("description")
        restaurant.address = request.POST.get("address")
        restaurant.save()

        return redirect("restaurants:detail", id=restaurant.id)
 
    context = {
        "restaurant": restaurant,
        "categories": Category.objects.all(),
        "locations": Location.objects.all(),
    }

    return render(request, "restaurants/edit_restaurant.html", context)