from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Transaction


class TransactionListView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = 'expense_tracker/home.html'
    context_object_name = 'transactions'
    paginate_by = 10

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user).order_by('-date')


class TransactionCreateView(LoginRequiredMixin, CreateView):
    model = Transaction
    fields = ['description','transaction_type','amount','date']
    success_url = reverse_lazy('tracker-home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TransactionUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Transaction
    fields = ['description','transaction_type','amount','date']
    success_url = reverse_lazy('tracker-home')

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
    success_url = reverse_lazy('tracker-home')

    def test_func(self):
        transaction = self.get_object()
        if self.request.user == transaction.user:
            return True
        return False


def about(request):
    context = {
        'title': 'About'
    }
    return render(request, 'expense_tracker/about.html', context)
