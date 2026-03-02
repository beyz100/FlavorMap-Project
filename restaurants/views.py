from django.shortcuts import render

def home_view(request):
    context = {
        'title': 'FlavorMap - Home',
        'welcome_message': 'Ready to discover the best restaurants?'
    }
    return render(request, 'restaurants/home.html', context)

def restaurant_list_view(request):
    restaurants = [
        {'id': 1, 'name': 'KFC', 'category': 'Fast Food', 'rating': 4.5},
        {'id': 2, 'name': 'Sushico', 'category': 'Asian', 'rating': 4.8},
        {'id': 3, 'name': 'Develi', 'category': 'Turkish', 'rating': 4.9},
    ]
    return render(request, 'restaurants/list.html', {'restaurants': restaurants})

def restaurant_detail_view(request, id):
    restaurant = {
        'id': id,
        'name': 'Sample Restaurant',
        'description': 'Description of the amazing food here.',
        'rating': 4.7,
        'address': 'Bayside, Snake Hills'
    }
    return render(request, 'restaurants/detail.html', {'restaurant': restaurant})

def about_view(request):
    return render(request, 'restaurants/about.html', {'title': 'About Us'})

def contact_view(request):
    return render(request, 'restaurants/contact.html', {'title': 'Contact'})
