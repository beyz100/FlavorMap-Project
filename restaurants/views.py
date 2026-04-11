from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.db.models import Avg

from .models import Category, Favorite, Location, Restaurant, Review, MenuItem
from .forms import RestaurantForm, MenuItemForm


def _user_owns_restaurant(user, restaurant):
    return restaurant.owner_id is not None and restaurant.owner_id == user.pk


def home(request):
    featured_restaurants = Restaurant.objects.select_related('category').order_by("-id")[:3]
    return render(request, "restaurants/home.html", {"restaurants": featured_restaurants})


def restaurant_list(request):
    query = request.GET.get("q")
    category = request.GET.get("category")
    location = request.GET.get("location")
    price = request.GET.get("price")

    restaurants = Restaurant.objects.select_related('category', 'location').annotate(
        annotated_avg_rating=Avg('reviews__rating')
    )

    if query:
        restaurants = restaurants.filter(name__icontains=query)

    if category:
        restaurants = restaurants.filter(category_id=category)

    if location:
        restaurants = restaurants.filter(location_id=location)

    if price:
        restaurants = restaurants.filter(price_range=price)

    categories = Category.objects.all()
    locations = Location.objects.all()

    return render(request, "restaurants/list.html", {
        "restaurants": restaurants,
        "categories": categories,
        "locations": locations,
    })


def restaurant_detail(request, id):
    restaurant = get_object_or_404(Restaurant, id=id)

    menu_items = restaurant.menu_items.all()
    reviews = restaurant.reviews.all().order_by("-created_at")

    is_favorite = False
    can_manage_restaurant = False
    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(
            user=request.user, restaurant=restaurant
        ).exists()
        can_manage_restaurant = _user_owns_restaurant(request.user, restaurant)

    context = {
        "restaurant": restaurant,
        "menu_items": menu_items,
        "reviews": reviews,
        "is_favorite": is_favorite,
        "can_manage_restaurant": can_manage_restaurant,
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
        form = RestaurantForm(request.POST, request.FILES)
        if form.is_valid():
            restaurant = form.save(commit=False)
            restaurant.owner = request.user
            restaurant.save()
            return redirect("restaurants:detail", id=restaurant.id)
    else:
        form = RestaurantForm()

    return render(request, "restaurants/create_restaurant.html", {"form": form})


@login_required
def edit_restaurant(request, id):
    restaurant = get_object_or_404(Restaurant, id=id)

    if not _user_owns_restaurant(request.user, restaurant):
        messages.error(
            request,
            "You can only edit restaurants you created.",
        )
        return redirect("restaurants:detail", id=id)

    if request.method == "POST":
        form = RestaurantForm(request.POST, request.FILES, instance=restaurant)
        if form.is_valid():
            form.save()
            return redirect("restaurants:detail", id=restaurant.id)
    else:
        form = RestaurantForm(instance=restaurant)

    return render(request, "restaurants/edit_restaurant.html", {"form": form, "restaurant": restaurant})


@login_required
@require_POST
def delete_restaurant(request, id):
    restaurant = get_object_or_404(Restaurant, id=id)

    if not _user_owns_restaurant(request.user, restaurant):
        messages.error(
            request,
            "You can only delete restaurants you created.",
        )
        return redirect("restaurants:detail", id=id)

    restaurant.delete()
    messages.success(request, "Restaurant removed.")
    return redirect("restaurants:list")


@login_required
def add_menu_item(request, id):
    restaurant = get_object_or_404(Restaurant, id=id)

    if not _user_owns_restaurant(request.user, restaurant):
        messages.error(request, "You can only add menu items to restaurants you created.")
        return redirect("restaurants:detail", id=id)

    if request.method == "POST":
        form = MenuItemForm(request.POST)
        if form.is_valid():
            menu_item = form.save(commit=False)
            menu_item.restaurant = restaurant
            menu_item.save()
            return redirect("restaurants:detail", id=restaurant.id)
    else:
        form = MenuItemForm()

    return render(request, "restaurants/add_menu_item.html", {"form": form, "restaurant": restaurant})


@login_required
def delete_menu_item(request, id):
    menu_item = get_object_or_404(MenuItem, id=id)
    restaurant = menu_item.restaurant

    if not _user_owns_restaurant(request.user, restaurant):
        messages.error(request, "You can only delete menu items from restaurants you created.")
        return redirect("restaurants:detail", id=restaurant.id)

    menu_item.delete()
    return redirect("restaurants:detail", id=restaurant.id)


@login_required
def edit_menu_item(request, id):
    menu_item = get_object_or_404(MenuItem, id=id)
    restaurant = menu_item.restaurant

    if not _user_owns_restaurant(request.user, restaurant):
        messages.error(request, "You can only edit menu items of restaurants you created.")
        return redirect("restaurants:detail", id=restaurant.id)

    if request.method == "POST":
        form = MenuItemForm(request.POST, instance=menu_item)
        if form.is_valid():
            form.save()
            return redirect("restaurants:detail", id=restaurant.id)
    else:
        form = MenuItemForm(instance=menu_item)

    return render(request, "restaurants/edit_menu_item.html", {"form": form, "menu_item": menu_item})
