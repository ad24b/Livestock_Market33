from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.middleware.csrf import rotate_token
from django.contrib import messages
from .forms import UserRegistrationForm, UserLoginForm, ProfileUpdateForm
from livestock.models import Livestock
from .models import SellerRequest, CustomUser
from .forms import SellerRequestForm
from django.contrib.sessions.models import Session
from django.utils import timezone

### ✅ تسجيل مستخدم جديد (بشكل افتراضي كزبون)
def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'buyer'  # تعيين المستخدم كزبون بشكل افتراضي
            user.save()
            messages.success(request, 'تم تسجيل حسابك بنجاح! يمكنك الآن تسجيل الدخول.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})


### ✅ تسجيل الدخول مع تحديث الجلسة و CSRF Token
def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            logout(request)  # ✅ تسجيل الخروج من أي جلسة نشطة
            request.session.flush()  # ✅ إنهاء الجلسة الحالية
            login(request, user)  # ✅ تسجيل الدخول للمستخدم الجديد
            
            # ✅ إنشاء جلسة جديدة وتحديث CSRF
            request.session.cycle_key()
            rotate_token(request)
            messages.success(request, f'مرحبًا {user.username}! تم تسجيل دخولك بنجاح.')
            return redirect('profile')
    else:
        form = UserLoginForm()
    return render(request, 'users/login.html', {'form': form})



### ✅ تسجيل الخروج بشكل آمن مع إنهاء الجلسة
def logout_view(request):
    logout(request)
    request.session.flush()  # ✅ حذف الجلسة بالكامل
    messages.success(request, 'تم تسجيل خروجك بنجاح.')
    return redirect('login')



### ✅ عرض الملف الشخصي مع إمكانية عرض ملف مستخدم آخر
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


### ✅ عرض الصفحة الرئيسية
def home_view(request):
    return render(request, 'users/home.html')


### ✅ تعديل الملف الشخصي (رفع الصورة وتحديث المعلومات)
@login_required
def edit_profile_view(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'تم تحديث ملفك الشخصي بنجاح.')
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, 'users/edit_profile.html', {'form': form})


### ✅ تقديم طلب للتحول إلى بائع
@login_required
def become_seller_request_view(request):
    if request.user.role == 'seller':
        messages.info(request, 'أنت بالفعل بائع.')
        return redirect('profile')

    if SellerRequest.objects.filter(user=request.user).exists():
        messages.info(request, 'لقد أرسلت طلبًا مسبقًا.')
        return redirect('profile')

    if request.method == 'POST':
        form = SellerRequestForm(request.POST)
        if form.is_valid():
            seller_request = form.save(commit=False)
            seller_request.user = request.user
            seller_request.save()
            messages.success(request, 'تم إرسال طلبك بنجاح، بانتظار الموافقة.')
            return redirect('profile')
    else:
        form = SellerRequestForm()

    return render(request, 'users/become_seller_request.html', {'form': form})
