from django.shortcuts import render
from products.models import products

def home(request):
    featured = products.objects.filter(featured=1)
    
    return render(request, 'Kavraz/index.html',
                  {'featured':featured           
    })

def about(request):
    return render(request, 'Kavraz/about.html')
