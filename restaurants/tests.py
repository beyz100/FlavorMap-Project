from django.test import TestCase
from django.urls import reverse

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
        self.assertContains(response, 'Burger King')

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
