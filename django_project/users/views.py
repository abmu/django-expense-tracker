from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.views import View
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


class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, View):

    def post(self, request, username):
        u = User.objects.filter(username=username)
        u.delete()
        messages.success(request, f'Your account has been deleted!')
        return redirect('login')
    
    def get(self, request, username):
        return render(request, 'users/delete_account.html')

    def test_func(self):
        if self.request.user.username == self.kwargs['username']:
            return True
        return False