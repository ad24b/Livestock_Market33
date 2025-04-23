from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .forms import UserRegistrationForm, UserLoginForm, ProfileUpdateForm
from livestock.models import Livestock
from .models import CustomUser  # تأكد من إضافة هذا

def register_view(response):
    if response.method == 'POST':
        form = UserRegistrationForm(response.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(response, 'users/register.html', {'form': form})

def login_view(response):
    if response.method == 'POST':
        form = UserLoginForm(data=response.POST)
        if form.is_valid():
            user = form.get_user()
            login(response, user)
            return redirect('profile')  # بعد الدخول يذهب إلى الملف الشخصي
    else:
        form = UserLoginForm()
    return render(response, 'users/login.html', {'form': form})

def logout_view(response):
    logout(response)
    return redirect('login')

# ✅ تعديل هذا العرض ليعرض ملف مستخدم آخر عند تمرير ?user=username
@login_required
def profile_view(request):
    username = request.GET.get('user')
    if username:
        user = get_object_or_404(CustomUser, username=username)
    else:
        user = request.user

    products = Livestock.objects.filter(seller=user)

    context = {
        'user_profile': user,
        'products': products,
    }
    return render(request, 'users/profile.html', context)

def home_view(response):
    return render(response, 'users/home.html')

@login_required
def edit_profile_view(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, 'users/edit_profile.html', {'form': form})
