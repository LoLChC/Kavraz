from django.shortcuts import render
from products.models import products
import random

def home(request):
    featured = products.objects.filter(featured=1)
    
    return render(request, 'Kavraz/index.html',
                  {'featured':featured,
                   "random_number": random.randint(1, 1000)
    })

def about(request):
    return render(request, 'Kavraz/about.html',
                  {"random_number": random.randint(1, 1000)
    })
