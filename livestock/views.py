from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from .forms import LivestockForm
from .models import Livestock

# وظيفة إضافية لتحرير الحجوزات المنتهية
def release_expired_reservations():
    expired_items = Livestock.objects.filter(reserved=True, reserved_until__lt=timezone.now())
    for item in expired_items:
        item.reserved = False
        item.reserved_until = None
        item.reserved_by = None
        item.save()

@login_required
def add_livestock_view(request):
    if request.method == 'POST':
        form = LivestockForm(request.POST, request.FILES)
        if form.is_valid():
            livestock = form.save(commit=False)
            livestock.seller = request.user
            livestock.save()
            return redirect('list_livestock')  # الانتقال إلى قائمة المواشي بعد الإضافة
    else:
        form = LivestockForm()
    return render(request, 'livestock/add_livestock.html', {'form': form})

def list_livestock_view(request):
    release_expired_reservations()  # ← هنا التأكد من الحجوزات المنتهية
    livestock = Livestock.objects.filter(reserved=False)  # عرض المواشي الغير محجوزة فقط
    return render(request, 'livestock/list_livestock.html', {'livestock': livestock})

def livestock_detail(request, pk):
    livestock = get_object_or_404(Livestock, pk=pk)  # جلب المنتج بناءً على المفتاح الأساسي
    return render(request, 'livestock/detail.html', {'livestock': livestock})



