from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from fib.models import Fibonacci

def show_fibo(request):
    fibo = Fibonacci.objects.all()
    numbers = [fib.value for fib in fibo]
    return HttpResponse(numbers)
