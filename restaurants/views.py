from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.db.models import Avg, Q
from django.db import transaction

from .forms import MenuItemForm, OpeningHoursForm, ReplyForm, RestaurantForm, ReviewForm, RestaurantPhotoForm
from .models import Category, Favorite, Location, OpeningHours, Restaurant, Review, MenuItem, RestaurantPhoto


def _user_owns_restaurant(user, restaurant):
    return restaurant.owner_id is not None and restaurant.owner_id == user.pk


def home(request):
    top_rated = (
        Restaurant.objects.select_related('category', 'location')
        .annotate(avg_rating=Avg('reviews__rating'))
        .order_by('-avg_rating')[:3]
    )
    newest = (
        Restaurant.objects.select_related('category', 'location')
        .order_by('-id')[:3]
    )
    return render(request, "restaurants/home.html", {
        "top_rated": top_rated,
        "newest": newest,
    })


def restaurant_list(request):
    query = request.GET.get("q")
    category = request.GET.get("category")
    location = request.GET.get("location")
    price = request.GET.get("price")

    restaurants = Restaurant.objects.select_related('category', 'location').annotate(
        annotated_avg_rating=Avg('reviews__rating')
    )

    sort = request.GET.get("sort")

    if query:
        restaurants = restaurants.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(location__name__icontains=query)
        )

    if category:
        restaurants = restaurants.filter(category_id=category)

    if location:
        restaurants = restaurants.filter(location_id=location)

    if price:
        restaurants = restaurants.filter(price_range=price)

    if sort == "rating":
        restaurants = restaurants.order_by("-annotated_avg_rating")

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
    reviews = restaurant.reviews.filter(parent__isnull=True).order_by("-created_at")
    review_form = ReviewForm()
    opening_hours = restaurant.opening_hours.all()
    gallery_photos = restaurant.gallery_photos.all()

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
        "opening_hours": opening_hours,
        "gallery_photos": gallery_photos,
        "reviews": reviews,
        "is_favorite": is_favorite,
        "can_manage_restaurant": can_manage_restaurant,
        "review_form": review_form,
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
    form = ReviewForm(request.POST)

    if not form.is_valid():
        messages.error(request, "Invalid input.")
        return redirect("restaurants:detail", id=id)

    try:
        with transaction.atomic():
            if Review.objects.filter(
                restaurant=restaurant,
                user=request.user,
                parent__isnull=True
            ).exists():
                messages.error(request, "You have already reviewed this restaurant.")
                return redirect("restaurants:detail", id=id)

            review = form.save(commit=False)
            review.restaurant = restaurant
            review.user = request.user
            review.parent = None
            review.save()

    except IntegrityError:
        messages.error(request, "A database error occurred while saving your review.")
        return redirect("restaurants:detail", id=id)

    messages.success(request, "Review added.")
    return redirect("restaurants:detail", id=id)

@login_required
def edit_review(request, id):
    review = get_object_or_404(Review, id=id, parent__isnull=True)

    if review.user != request.user:
        messages.error(request, "You can only edit your own reviews.")
        return redirect("restaurants:detail", id=review.restaurant.id)

    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, "Review updated.")
            return redirect("restaurants:detail", id=review.restaurant.id)
    else:
        form = ReviewForm(instance=review)

    return render(request, "restaurants/edit_review.html", {
        "form": form,
        "review": review,
    })


@login_required
@require_POST
def delete_review(request, id):
    review = get_object_or_404(Review, id=id)

    if review.user != request.user:
        messages.error(request, "You can only delete your own reviews.")
        return redirect("restaurants:detail", id=review.restaurant.id)

    restaurant_id = review.restaurant.id
    review.delete()
    messages.success(request, "Review deleted.")
    return redirect("restaurants:detail", id=restaurant_id)


@login_required
@require_POST
def add_reply(request, id):
    parent_review = get_object_or_404(Review, id=id, parent__isnull=True)
    form = ReplyForm(request.POST)

    if not form.is_valid():
        messages.error(request, "Reply cannot be empty.")
        return redirect("restaurants:detail", id=parent_review.restaurant.id)

    try:
        with transaction.atomic():
            reply = form.save(commit=False)
            reply.restaurant = parent_review.restaurant
            reply.user = request.user
            reply.parent = parent_review
            reply.rating = None
            reply.save()

    except IntegrityError:
        messages.error(request, "A database error occurred while saving your reply.")
        return redirect("restaurants:detail", id=parent_review.restaurant.id)

    messages.success(request, "Reply added.")
    return redirect("restaurants:detail", id=parent_review.restaurant.id)


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


@login_required
def add_opening_hours(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)

    if not _user_owns_restaurant(request.user, restaurant):
        messages.error(request, "You can only edit restaurants you created.")
        return redirect("restaurants:detail", id=restaurant.id)

    if request.method == "POST":
        form = OpeningHoursForm(request.POST)
        if form.is_valid():
            opening_hours = form.save(commit=False)
            opening_hours.restaurant = restaurant
            try:
                opening_hours.save()
            except IntegrityError:
                form.add_error("day", "Opening hours for this day already exist. Edit the existing entry.")
            else:
                messages.success(request, "Opening hours added.")
                return redirect("restaurants:detail", id=restaurant.id)
    else:
        form = OpeningHoursForm()

    return render(
        request,
        "restaurants/add_opening_hours.html",
        {
            "form": form,
            "restaurant": restaurant,
        },
    )


@login_required
def edit_opening_hours(request, id):
    opening_hours = get_object_or_404(OpeningHours, id=id)
    restaurant = opening_hours.restaurant

    if not _user_owns_restaurant(request.user, restaurant):
        messages.error(request, "You can only edit restaurants you created.")
        return redirect("restaurants:detail", id=restaurant.id)

    if request.method == "POST":
        form = OpeningHoursForm(request.POST, instance=opening_hours)
        if form.is_valid():
            try:
                form.save()
            except IntegrityError:
                form.add_error("day", "Opening hours for this day already exist.")
            else:
                messages.success(request, "Opening hours updated.")
                return redirect("restaurants:detail", id=restaurant.id)
    else:
        form = OpeningHoursForm(instance=opening_hours)

    return render(
        request,
        "restaurants/edit_opening_hours.html",
        {"form": form, "restaurant": restaurant, "opening_hours": opening_hours},
    )


@login_required
@require_POST
def delete_opening_hours(request, id):
    opening_hours = get_object_or_404(OpeningHours, id=id)
    restaurant = opening_hours.restaurant

    if not _user_owns_restaurant(request.user, restaurant):
        messages.error(request, "You can only edit restaurants you created.")
        return redirect("restaurants:detail", id=restaurant.id)

    opening_hours.delete()
    messages.success(request, "Opening hours removed.")
    return redirect("restaurants:detail", id=restaurant.id)

@login_required
def add_photo(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)

    if not _user_owns_restaurant(request.user, restaurant):
        messages.error(request, "You can only add photos to restaurants you created.")
        return redirect("restaurants:detail", id=restaurant.id)

    if request.method == "POST":
        form = RestaurantPhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.restaurant = restaurant
            photo.save()
            messages.success(request, "Photo added to gallery.")
            return redirect("restaurants:detail", id=restaurant.id)
    else:
        form = RestaurantPhotoForm()

    return render(request, "restaurants/add_photo.html", {"form": form, "restaurant": restaurant})

@login_required
@require_POST
def delete_photo(request, id):
    photo = get_object_or_404(RestaurantPhoto, id=id)
    restaurant = photo.restaurant

    if not _user_owns_restaurant(request.user, restaurant):
        messages.error(request, "You can only delete photos of restaurants you created.")
        return redirect("restaurants:detail", id=restaurant.id)

    photo.delete()
    messages.success(request, "Photo removed from gallery.")
    return redirect("restaurants:detail", id=restaurant.id)