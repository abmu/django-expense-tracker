from django.shortcuts import render
from django.http import HttpResponse

purchases = [
    {
        'user': 'AbdulM',
        'item': 'Item 1',
        'cost': '£4.99',
        'date': 'June 24, 2023'
    },
    {
        'user': 'AbdulM',
        'item': 'Item 1',
        'cost': '£4.99',
        'date': 'June 24, 2023'
    }
]


def home(request):
    context = {
        'purchases': purchases
    }
    return render(request, 'expense_tracker/home.html', context)


def about(request):
    return render(request, 'expense_tracker/about.html', {'title': 'About'})
