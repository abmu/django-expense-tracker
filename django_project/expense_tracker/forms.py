from django import forms
from django.forms import ModelForm
from django.forms.widgets import DateInput
from .models import Transaction


class TransactionForm(ModelForm):

    class Meta:
        model = Transaction
        fields = ['description','transaction_type','amount','date']
        widgets = {
            'date': DateInput(attrs={'type': 'date'}),
        }
