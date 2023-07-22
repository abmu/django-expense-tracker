from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account successfully created for {username}!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def settings(request):
    return render(request, 'users/settings.html', {'title': 'Settings'})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('settings')
    else:
        u_form = UserUpdateForm(instance=request.user)
    return render(request, 'users/profile.html', {'u_form': u_form})


# class TransactionUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
#     model = Transaction
#     form_class = TransactionForm
#     success_url = reverse_lazy('transaction-history')

#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         return super().form_valid(form)
    
#     def test_func(self):
#         transaction = self.get_object()
#         if self.request.user == transaction.user:
#             return True
#         return False
@login_required
def delete(request, username):
    if request.method == 'POST':
        u = User.objects.filter(username=username)
        u.delete()
        messages.success(request, f'Your account has been deleted!')
        return redirect('login')
    return render(request, 'users/delete_account.html')