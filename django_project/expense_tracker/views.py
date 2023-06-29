from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Purchase


@login_required(redirect_field_name=None)
def home(request):
    context = {
        'purchases': Purchase.objects.all()
    }
    return render(request, 'expense_tracker/home.html', context)


def about(request):
    return render(request, 'expense_tracker/about.html', {'title': 'About'})
