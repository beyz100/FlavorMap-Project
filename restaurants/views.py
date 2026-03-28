from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .models import Favorite, Restaurant, Review


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