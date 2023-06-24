from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    return render(request, 'expense_tracker/home.html')


def about(request):
    return render(request, 'expense_tracker/about.html')
