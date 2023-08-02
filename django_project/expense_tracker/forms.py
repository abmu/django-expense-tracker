from django import forms
from django.db import models
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


class TransactionFilterForm(ModelForm):
    start_date = forms.DateField(widget=forms.DateInput(attrs=dict(type='date')))
    end_date = forms.DateField(widget=forms.DateInput(attrs=dict(type='date')))

    class Meta:
        model = Transaction
        fields = ['description','transaction_type','amount','start_date','end_date']
        widgets = {
            'start_date': DateInput(attrs={'type': 'date'}),
            'end_date': DateInput(attrs={'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        super(TransactionFilterForm, self).__init__(*args, **kwargs)
        # set all fields as not required
        for field in self.fields:
            self.fields[field].required = False


class ContactForm(forms.Form):
    subject = forms.CharField(max_length=50, 
                              label='Subject',
                              widget=forms.TextInput(attrs={'placeholder': 'Subject'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Message'}))
    