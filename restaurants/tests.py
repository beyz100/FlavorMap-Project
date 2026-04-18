from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Category, Favorite, Location, OpeningHours, Restaurant, MenuItem, Review

class MS1ViewsTest(TestCase):
    
    def setUp(self):
        self.category = Category.objects.create(name='Fast Food')
        self.location = Location.objects.create(name='Test City')
        self.restaurant = Restaurant.objects.create(
            name='KFC',
            category=self.category,
            location=self.location,
            description='Finger lickin good',
            address='123 Test Ave'
        )

    def test_home_view(self):
        response = self.client.get(reverse('restaurants:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Welcome to FlavorMap!')

    def test_restaurant_list_view(self):
        response = self.client.get(reverse('restaurants:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'KFC')

    def test_restaurant_detail_view(self):
        response = self.client.get(reverse('restaurants:detail', args=[self.restaurant.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'KFC')
        
    def test_about_view(self):
        response = self.client.get(reverse('restaurants:about'))
        self.assertEqual(response.status_code, 200)

    def test_contact_view(self):
        response = self.client.get(reverse('restaurants:contact'))
        self.assertEqual(response.status_code, 200)

class MS2ModelsTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='pw')
        self.user2 = User.objects.create_user(username='user2', password='pw')
        
        self.category = Category.objects.create(name='Fast Food')
        self.location = Location.objects.create(name='Downtown')
        
        self.restaurant = Restaurant.objects.create(
            name='Test Burger',
            category=self.category,
            location=self.location,
            description='Great burgers',
            address='123 Test St'
        )
        
        self.menu_item = MenuItem.objects.create(
            restaurant=self.restaurant,
            name='Cheeseburger',
            description='Classic cheese',
            price=5.99
        )

    def test_category_creation(self):
        self.assertEqual(self.category.name, 'Fast Food')

    def test_location_creation(self):
        self.assertEqual(self.location.name, 'Downtown')

    def test_restaurant_creation(self):
        self.assertEqual(self.restaurant.name, 'Test Burger')
        self.assertEqual(self.restaurant.location.name, 'Downtown')

    def test_menu_item_creation(self):
        self.assertEqual(self.menu_item.name, 'Cheeseburger')
        self.assertEqual(self.menu_item.price, 5.99)

    def test_average_rating_with_reviews(self):
        Review.objects.create(restaurant=self.restaurant, user=self.user1, rating=4, comment='Good')
        Review.objects.create(restaurant=self.restaurant, user=self.user2, rating=5, comment='Excellent')
        self.assertEqual(self.restaurant.average_rating(), 4.5)

    def test_average_rating_without_reviews(self):
        self.assertEqual(self.restaurant.average_rating(), 0.0)


class AuthProfileTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="profileuser", password="secret123")
        self.category = Category.objects.create(name="Cafe")
        self.location = Location.objects.create(name="Center")
        self.restaurant = Restaurant.objects.create(
            name="Cafe M",
            category=self.category,
            location=self.location,
            description="Coffee",
            address="1 Main St",
        )
        Review.objects.create(
            restaurant=self.restaurant,
            user=self.user,
            rating=5,
            comment="Great espresso",
        )
        Favorite.objects.create(user=self.user, restaurant=self.restaurant)

    def test_profile_redirects_when_not_logged_in(self):
        response = self.client.get(reverse("restaurants:profile"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(response.url.split("?")[0], "/accounts/login/")

    def test_profile_lists_reviews_and_favorites_when_logged_in(self):
        self.client.login(username="profileuser", password="secret123")
        response = self.client.get(reverse("restaurants:profile"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Great espresso")
        self.assertContains(response, "Cafe M")


class RestaurantOwnerAuthorizationTest(TestCase):

    def setUp(self):
        self.owner = User.objects.create_user(username="owner1", password="pass12345")
        self.other = User.objects.create_user(username="other1", password="pass12345")
        self.category = Category.objects.create(name="Diner")
        self.location = Location.objects.create(name="North")
        self.restaurant = Restaurant.objects.create(
            name="Owned Place",
            owner=self.owner,
            category=self.category,
            location=self.location,
            description="Food",
            address="9 Road",
        )

    def test_owner_can_open_edit_page(self):
        self.client.login(username="owner1", password="pass12345")
        r = self.client.get(
            reverse("restaurants:edit_restaurant", args=[self.restaurant.id])
        )
        self.assertEqual(r.status_code, 200)

    def test_non_owner_cannot_open_edit_page(self):
        self.client.login(username="other1", password="pass12345")
        r = self.client.get(
            reverse("restaurants:edit_restaurant", args=[self.restaurant.id]),
            follow=False,
        )
        self.assertEqual(r.status_code, 302)
        self.assertEqual(
            r.url, reverse("restaurants:detail", args=[self.restaurant.id])
        )

    def test_non_owner_cannot_delete(self):
        self.client.login(username="other1", password="pass12345")
        r = self.client.post(
            reverse("restaurants:delete_restaurant", args=[self.restaurant.id]),
        )
        self.assertEqual(r.status_code, 302)
        self.assertTrue(Restaurant.objects.filter(pk=self.restaurant.pk).exists())

    def test_owner_can_delete(self):
        self.client.login(username="owner1", password="pass12345")
        rid = self.restaurant.id
        r = self.client.post(reverse("restaurants:delete_restaurant", args=[rid]))
        self.assertEqual(r.status_code, 302)
        self.assertEqual(r.url, reverse("restaurants:list"))
        self.assertFalse(Restaurant.objects.filter(pk=rid).exists())


class OpeningHoursCrudAuthorizationTest(TestCase):

    def setUp(self):
        self.owner = User.objects.create_user(username="owner_oh", password="pass12345")
        self.other = User.objects.create_user(username="other_oh", password="pass12345")
        self.category = Category.objects.create(name="Brunch")
        self.location = Location.objects.create(name="South")
        self.restaurant = Restaurant.objects.create(
            name="Hours Place",
            owner=self.owner,
            category=self.category,
            location=self.location,
            description="Food",
            address="10 Street",
        )
        self.oh = OpeningHours.objects.create(
            restaurant=self.restaurant, day="weekdays", open_time="09:00", close_time="17:00"
        )

    def test_owner_can_add_opening_hours(self):
        self.client.login(username="owner_oh", password="pass12345")
        r = self.client.post(
            reverse("restaurants:add_opening_hours", args=[self.restaurant.id]),
            data={"day": "weekends", "open_time": "10:00", "close_time": "18:00"},
        )
        self.assertEqual(r.status_code, 302)
        self.assertTrue(
            OpeningHours.objects.filter(restaurant=self.restaurant, day="weekends").exists()
        )

    def test_owner_can_open_edit_opening_hours_page(self):
        self.client.login(username="owner_oh", password="pass12345")
        r = self.client.get(reverse("restaurants:edit_opening_hours", args=[self.oh.id]))
        self.assertEqual(r.status_code, 200)

    def test_owner_can_edit_opening_hours(self):
        self.client.login(username="owner_oh", password="pass12345")
        r = self.client.post(
            reverse("restaurants:edit_opening_hours", args=[self.oh.id]),
            data={"day": "weekdays", "open_time": "08:30", "close_time": "16:30"},
        )
        self.assertEqual(r.status_code, 302)
        self.oh.refresh_from_db()
        self.assertEqual(str(self.oh.open_time), "08:30:00")
        self.assertEqual(str(self.oh.close_time), "16:30:00")

    def test_non_owner_cannot_edit_opening_hours(self):
        self.client.login(username="other_oh", password="pass12345")
        r = self.client.get(
            reverse("restaurants:edit_opening_hours", args=[self.oh.id]),
            follow=False,
        )
        self.assertEqual(r.status_code, 302)

    def test_owner_can_delete_opening_hours(self):
        self.client.login(username="owner_oh", password="pass12345")
        oid = self.oh.id
        r = self.client.post(reverse("restaurants:delete_opening_hours", args=[oid]))
        self.assertEqual(r.status_code, 302)
        self.assertFalse(OpeningHours.objects.filter(pk=oid).exists())

    def test_non_owner_cannot_delete_opening_hours(self):
        self.client.login(username="other_oh", password="pass12345")
        oid = self.oh.id
        r = self.client.post(reverse("restaurants:delete_opening_hours", args=[oid]))
        self.assertEqual(r.status_code, 302)
        self.assertTrue(OpeningHours.objects.filter(pk=oid).exists())