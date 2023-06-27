from django.shortcuts import render
from .models import Purchase


def home(request):
    context = {
        'purchases': Purchase.objects.all()
    }
    return render(request, 'expense_tracker/home.html', context)


def about(request):
    return render(request, 'expense_tracker/about.html', {'title': 'About'})
