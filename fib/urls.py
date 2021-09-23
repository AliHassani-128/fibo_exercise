from django.urls import path

from fib.views import show_fibo

urlpatterns = [
    path('',show_fibo,name='show_fibo'),
]