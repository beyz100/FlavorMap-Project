from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .models import Category, Favorite, Location, Restaurant, Review, MenuItem


def home(request):
    featured_restaurants = Restaurant.objects.all().order_by("-id")[:3]
    return render(request, "restaurants/home.html", {"restaurants": featured_restaurants})


def restaurant_list(request):
    restaurants = Restaurant.objects.all()
    return render(request, "restaurants/list.html", {"restaurants": restaurants})


def restaurant_detail(request, id):
    restaurant = get_object_or_404(Restaurant, id=id)

    menu_items = restaurant.menu_items.all()
    reviews = restaurant.reviews.all().order_by("-created_at")

    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(
            user=request.user, restaurant=restaurant
        ).exists()

    context = {
        "restaurant": restaurant,
        "menu_items": menu_items,
        "reviews": reviews,
        "is_favorite": is_favorite,
    }
    return render(request, "restaurants/detail.html", context)


def about(request):
    return render(request, "restaurants/about.html")


def contact(request):
    return render(request, "restaurants/contact.html")


@login_required
def user_profile(request):
    reviews = request.user.review_set.select_related("restaurant").order_by(
        "-created_at"
    )
    favorites = request.user.favorites.select_related("restaurant").order_by(
        "-created_at"
    )
    return render(
        request,
        "restaurants/profile.html",
        {"reviews": reviews, "favorites": favorites},
    )


@login_required
@require_POST
def add_review(request, id):
    restaurant = get_object_or_404(Restaurant, id=id)
    try:
        rating = int(request.POST.get("rating", ""))
    except (TypeError, ValueError):
        rating = 0
    if rating not in range(1, 6):
        messages.error(request, "Please choose a rating from 1 to 5.")
        return redirect("restaurants:detail", id=id)

    comment = (request.POST.get("comment") or "").strip()
    if not comment:
        messages.error(request, "Please write a comment for your review.")
        return redirect("restaurants:detail", id=id)

    Review.objects.create(
        restaurant=restaurant,
        user=request.user,
        rating=rating,
        comment=comment,
    )
    messages.success(request, "Thanks — your review was posted.")
    return redirect("restaurants:detail", id=id)


@login_required
@require_POST
def toggle_favorite(request, id):
    restaurant = get_object_or_404(Restaurant, id=id)
    favorite, created = Favorite.objects.get_or_create(
        user=request.user, restaurant=restaurant
    )
    if not created:
        favorite.delete()
        messages.success(request, "Removed from your favorites.")
    else:
        messages.success(request, "Saved to your favorites.")
    return redirect("restaurants:detail", id=id)


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
            address=address,
        )

        return redirect("restaurants:detail", id=restaurant.id)

    categories = Category.objects.all()
    locations = Location.objects.all()

    context = {
        "categories": categories,
        "locations": locations,
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
    
def delete_restaurant(request, id):
    
    restaurant = get_object_or_404(Restaurant, id=id)
    restaurant.delete()
    return redirect('restaurants:list')


@login_required
def add_menu_item(request, id):
    restaurant = get_object_or_404(Restaurant, id=id)

    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        price = request.POST.get("price")

        MenuItem.objects.create(
            restaurant=restaurant,
            name=name,
            description=description,
            price=price
        )

        return redirect("restaurants:detail", id=restaurant.id)

    return render(request, "restaurants/add_menu_item.html", {"restaurant": restaurant})


@login_required
def delete_menu_item(request, id):
    menu_item = get_object_or_404(MenuItem, id=id)
    restaurant_id = menu_item.restaurant.id
    menu_item.delete()
    return redirect('restaurants:detail', id=restaurant_id)


@login_required
def edit_menu_item(request, id):
    menu_item = get_object_or_404(MenuItem, id=id)

    if request.method == "POST":
        menu_item.name = request.POST.get("name")
        menu_item.description = request.POST.get("description")
        menu_item.price = request.POST.get("price")
        menu_item.save()

        return redirect("restaurants:detail", id=menu_item.restaurant.id)

    return render(request, "restaurants/edit_menu_item.html", {"menu_item": menu_item})