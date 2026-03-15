from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Category, Location, Restaurant, MenuItem, Review

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