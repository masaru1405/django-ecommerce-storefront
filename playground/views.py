from django.shortcuts import render
from django.http import HttpResponse

def say_hello(request):
   context = {'name': 'Kaio'}
   return render(request, 'playground/hello.html', context)
