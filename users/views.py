from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from users import models
from users import forms
from django.views import View
from .models import User


class RegisterView(View):
    def get(self, request):
        register_form = forms.RegisterForm()
        context = {
            'form': register_form
        }
        return render(request, 'register.html', context=context)

    def post(self, request):
        register_form = forms.RegisterForm(data=request.POST, files=request.FILES)
        if register_form.is_valid():
            register_form.save()
            return redirect('login')
        else:
            context = {
                "form": register_form
            }
            return render(request, 'register.html', context=context)


class LoginView(View):
    def get(self, request):
        login_form = AuthenticationForm()
        context = {
            "form": login_form
        }
        return render(request, 'login.html', context=context)

    def post(self, request):
        login_form = AuthenticationForm(data=request.POST)
        if login_form.is_valid():
            account = login_form.get_user()
            login(request, account)
            return redirect('ListProducts')
        else:
            context = {
                "form": login_form
            }
            return render(request, 'login.html', context=context)


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect('product:home')


class ProfileView(View):
    def get(self, request):
        profile_form = User()
        context = {
            "profile_form": profile_form
        }
        return render(request, 'profile.html', context=context)


class ProfileUpdateView(View):
    def get(self, request):
        update_form = forms.EditProfileForm(instance=request.user)
        return render(request, 'profile_update.html', {'form': update_form})

    def post(self, request):
        update_form = forms.EditProfileForm(request.POST, request.FILES, instance=request.user)
        if update_form.is_valid():
            update_form.save()
            return redirect('users:profile')
        else:
            return render(request, 'profile_update.html', {'form': update_form})

