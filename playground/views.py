from django.shortcuts import render
from django.http import HttpResponse

from store.models import Customer, Product

def say_hello(request):
   queryset = Product.objects.values('id', 'title', 'collection__title')
   
   return render(request, 'playground/hello.html', {'products': list(queryset)})
