from django.shortcuts import render, redirect
from django.db.models import Sum
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Transaction
from .forms import TransactionForm, TransactionFilterForm, ContactForm


class TransactionListView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = 'expense_tracker/history.html'
    context_object_name = 'transactions'
    paginate_by = 10

    def get_queryset(self):
        # only pass values that are not None or '' as arguments to the filter method
        filters = {
            'description__contains': self.request.GET.get('description'),
            'transaction_type': self.request.GET.get('transaction_type'),
            'amount': self.request.GET.get('amount'),
            'date__gte': self.request.GET.get('start_date'),
            'date__lte': self.request.GET.get('end_date')
        }
        not_empty_filters = {k:v for k, v in filters.items() if v != None and v != ''}
        return Transaction.objects.filter(user=self.request.user, **not_empty_filters).order_by('-date', '-pk')
    
    def get_context_data(self, *args, **kwargs):
        context = super(TransactionListView, self).get_context_data(*args, **kwargs)
        context['title'] = 'History'
        f_form = TransactionFilterForm(self.request.GET)
        context['f_form'] = f_form
        context['income'] = self.get_income_total()
        context['expense'] = self.get_expense_total()
        return context
    
    def get_income_total(self):
        return float(self.get_queryset().filter(user=self.request.user, transaction_type='Income').aggregate(Sum('amount'))['amount__sum'] or 0)
    
    def get_expense_total(self):
        return float(self.get_queryset().filter(user=self.request.user, transaction_type='Expense').aggregate(Sum('amount'))['amount__sum'] or 0)


class TransactionCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Transaction
    form_class = TransactionForm
    success_url = reverse_lazy('transaction-history')
    success_message = 'New transaction successfully added!'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TransactionUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Transaction
    form_class = TransactionForm
    success_url = reverse_lazy('transaction-history')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        transaction = self.get_object()
        if self.request.user == transaction.user:
            return True
        return False


class TransactionDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Transaction
    success_url = reverse_lazy('transaction-history')

    def test_func(self):
        transaction = self.get_object()
        if self.request.user == transaction.user:
            return True
        return False


@login_required(redirect_field_name=None)
def home(request):
    transaction = Transaction()
    context = {
        'title': 'Home',
        'balance': transaction.get_balance(request.user),
        'income': transaction.get_income_total(request.user),
        'expense': transaction.get_expense_total(request.user),
        'transactions': Transaction.objects.filter(user=request.user).order_by('-date', '-pk')[:5]
    }
    return render(request, 'expense_tracker/home.html', context)


def about(request):
    context = {
        'title': 'About'
    }
    return render(request, 'expense_tracker/about.html', context)


@login_required
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            send_mail(
                form.cleaned_data.get('subject'),
                f'{form.cleaned_data.get("message")}\n\nUsername: {request.user.username}\nEmail: {request.user.email}',
                settings.EMAIL_HOST_USER,
                [settings.EMAIL_HOST_USER],
                fail_silently=False
            )
            messages.success(request, f'You have successfully sent an email!')
            return redirect('tracker-contact')
    else:
        form = ContactForm()
    return render(request, 'expense_tracker/contact.html', {'form': form})
