from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, reverse
from django.views import View
from .forms import LoginForm, OtpLoginForm, CheckOtpForm, AddressCreationForm
from random import randint
from django.utils.crypto import get_random_string
import ghasedakpack
from .models import Otp, User
from uuid import uuid4
SMS = ghasedakpack.Ghasedak("8d2e3992e8d776fd625943f77a9946b682e9b148ee316bd87365caa2905232d3")


# def user_login(request):
#     return render(request, 'account/login.html', {})


class UserLogin(View):
    def get(self, request):
        form = LoginForm()
        return render(request, "account/login.html", {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)
                next_page = request.GET.get('next')
                if next_page:
                    return redirect(next_page)
                return redirect('/')
            else:
                form.add_error('phone', 'invalid user data')
        else:
            form.add_error('phone', 'invalid data')

        return render(request, 'account/login.html', {'form': form})


class OtpLoginView(View):
    def get(self, request):
        form = OtpLoginForm()
        return render(request, "account/otp_login.html", {'form': form})

    def post(self, request):
        form = OtpLoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            randcode = randint(1000, 9999)
            SMS.verification({'receptor': cd["phone"], 'type': '1', 'template': 'pdi', 'param1': randcode})
            token = str(uuid4())
            Otp.objects.create(phone=cd['phone'], code=randcode, token=token)
            print(randcode)
            return redirect(reverse('account:check_otp') + f"?token={token}")
        else:
            form.add_error('phone', 'invalid data')

        return render(request, 'account/otp_login.html', {'form': form})


class CheckOtpView(View):
    def get(self, request):
        form = CheckOtpForm()
        return render(request, "account/check_otp.html", {'form': form})

    def post(self, request):
        token = request.GET.get('token')
        form = CheckOtpForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if Otp.objects.filter(code=cd['code'], token=token).exists():
                otp = Otp.objects.get(token=token)
                user, is_create = User.objects.get_or_create(phone=otp.phone)
                # user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                otp.delete()
                return redirect('/')
        else:
            form.add_error('phone', 'invalid data')

        return render(request, 'account/check_otp.html', {'form': form})


class AddAddressView(View):
    def post(self, request):
        form = AddressCreationForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            next_page = request.GET.get('next')
            if next_page:
                return redirect(next_page)

        return render(request, 'account/add_address.html', {'form': form})

    def get(self, request):
        form = AddressCreationForm()
        return render(request, 'account/add_address.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('/')
