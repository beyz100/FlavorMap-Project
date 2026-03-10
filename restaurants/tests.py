from django.test import TestCase
from django.urls import reverse
from .models import Category, Restaurant, Review
from django.contrib.auth.models import User

class MS1ViewsTest(TestCase):

    def test_home_view(self):
        response = self.client.get(reverse('restaurants:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'restaurants/home.html')
        self.assertContains(response, 'Ready to discover')

    def test_restaurant_list_view(self):
        response = self.client.get(reverse('restaurants:list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'restaurants/list.html')
        self.assertContains(response, 'KFC')

    def test_restaurant_detail_view(self):
        response = self.client.get(reverse('restaurants:detail', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'restaurants/detail.html')
        self.assertContains(response, 'Sample Restaurant')

    def test_about_view(self):
        response = self.client.get(reverse('restaurants:about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'restaurants/about.html')

    def test_contact_view(self):
        response = self.client.get(reverse('restaurants:contact'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'restaurants/contact.html')


class MS2ModelsTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.category = Category.objects.create(name='Fast Food')
        self.restaurant = Restaurant.objects.create(
            name='Test Burger',
            category=self.category,
            description='Great burgers',
            address='123 Test St',
            rating=4.5
        )

    def test_category_creation(self):
        self.assertEqual(self.category.name, 'Fast Food')

    def test_restaurant_creation(self):
        self.assertEqual(self.restaurant.name, 'Test Burger')
        self.assertEqual(self.restaurant.category.name, 'Fast Food')

    def test_review_creation(self):
        review = Review.objects.create(
            restaurant=self.restaurant,
            user=self.user,
            rating=5,
            comment='Amazing!'
        )
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.restaurant, self.restaurant)